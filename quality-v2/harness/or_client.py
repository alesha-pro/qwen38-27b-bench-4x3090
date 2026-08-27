#!/usr/bin/env python3
"""OpenRouter client for the BF16 reference runs (quant-bench-v2).

Hard requirements (decisions 2026-08-22):
- model qwen/qwen3.8-27b, provider PINNED to AkashML, quantizations=["bf16"],
  allow_fallbacks=False. Without the pin the reference silently becomes FP8.
- Sampling per the official Qwen3.8 model card:
    thinking efforts (low/medium/xhigh): temperature=1.0 top_p=0.95 top_k=20
    off: temperature=0.7 top_p=0.80 top_k=20 presence_penalty=1.5
- No token caps: let the model stop naturally (max_tokens only as the
  endpoint ceiling guard).
- Full trace of every attempt is saved by the caller (we return everything).
"""
import json
import os
import time
import urllib.request
import urllib.error

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "qwen/qwen3.8-27b"

# Local-endpoint mode for the canary: point this same client at a rig /v1 so
# requests are built by the same code path and records land in the same shape,
# which lets score_run.py score both arms identically.
LOCAL_BASE = os.environ.get("QB2_LOCAL_BASE_URL", "")
LOCAL_MODEL = os.environ.get("QB2_LOCAL_MODEL", "qwen3.8-27b")

SAMPLING_THINKING = {"temperature": 1.0, "top_p": 0.95, "top_k": 20,
                     "presence_penalty": 0.0, "repetition_penalty": 1.0}
SAMPLING_OFF = {"temperature": 0.7, "top_p": 0.80, "top_k": 20,
                "presence_penalty": 1.5}

# How to express reasoning effort towards the provider. The provider runs the
# open Qwen3.8 weights whose native knob is reasoning_effort low/medium/xhigh.
# OpenRouter's portable field is reasoning.effort (minimal/low/medium/high).
# effort_mode:
#   "openrouter" -> {"reasoning": {"effort": low|medium|high}} (xhigh->high)
#   "raw"        -> passthrough {"reasoning_effort": "low|medium|xhigh"}
# The smoke test decides which mode actually reaches the model.
EFFORT_OR_MAP = {"low": "low", "medium": "medium", "xhigh": "high"}


def api_key() -> str:
    k = os.environ.get("OPENROUTER_API_KEY", "")
    if not k:
        p = os.path.expanduser("~/.config/openrouter/key")
        if os.path.exists(p):
            k = open(p).read().strip()
    if not k:
        raise RuntimeError(
            "No OpenRouter key: set OPENROUTER_API_KEY or put it in "
            "~/.config/openrouter/key")
    return k


def build_body(messages, effort, effort_mode="raw", tools=None,
               max_tokens=None):
    body = {
        "model": MODEL,
        "messages": messages,
        "provider": {
            "order": ["AkashML"],
            "allow_fallbacks": False,
            "quantizations": ["bf16"],
        },
        "usage": {"include": True},
    }
    if effort == "off":
        body.update(SAMPLING_OFF)
        body["reasoning"] = {"enabled": False}
    else:
        body.update(SAMPLING_THINKING)
        if effort_mode == "openrouter":
            body["reasoning"] = {"effort": EFFORT_OR_MAP[effort]}
        elif effort_mode == "raw":
            body["reasoning_effort"] = effort
        else:
            raise ValueError(f"bad effort_mode {effort_mode}")
    if tools:
        body["tools"] = tools
    if max_tokens:
        body["max_tokens"] = max_tokens
    if LOCAL_BASE:
        body["model"] = LOCAL_MODEL
        body.pop("provider", None)
        body.pop("usage", None)
        if body.pop("reasoning", None) is not None:
            # vLLM has no portable reasoning field; off-mode goes through
            # the chat template instead. Sampling stays untouched.
            body["chat_template_kwargs"] = {"enable_thinking": False}
        # llama-server knows nothing about a top-level reasoning_effort: for
        # Qwen3.8 the knob is only a line the chat template injects, so the
        # value has to ride in chat_template_kwargs instead. Same knob, same
        # rendered prompt, different envelope. vLLM keeps the top-level field.
        if os.environ.get("QB2_EFFORT_TRANSPORT") == "chat_template_kwargs":
            eff = body.pop("reasoning_effort", None)
            if eff is not None:
                body.setdefault("chat_template_kwargs", {})["reasoning_effort"] = eff
    return body


def chat(messages, effort, effort_mode="raw", tools=None, max_tokens=None,
         timeout=3600, retries=5):
    """One completion. Returns dict: {request, response, latency_s, error}."""
    body = build_body(messages, effort, effort_mode, tools, max_tokens)
    data = json.dumps(body).encode()
    last_err = None
    if LOCAL_BASE:
        url = LOCAL_BASE.rstrip("/") + "/chat/completions"
        headers = {"Content-Type": "application/json"}
    else:
        url = API_URL
        headers = {
            "Authorization": f"Bearer {api_key()}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/alesha-pro/4x3090-llm-benchmarks",
            "X-Title": "quant-bench-v2",
        }
    for attempt in range(retries):
        req = urllib.request.Request(url, data=data, headers=headers)
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                resp = json.loads(r.read())
            lat = time.time() - t0
            # OpenRouter can return 200 with an error payload
            if "error" in resp and "choices" not in resp:
                raise RuntimeError(f"payload error: {resp['error']}")
            # Guard: verify the pin actually held
            prov = resp.get("provider", "")
            if not LOCAL_BASE and prov and prov.lower() != "akashml":
                raise RuntimeError(f"PIN VIOLATION: served by {prov!r}")
            return {"request": body, "response": resp, "latency_s": lat,
                    "error": None}
        except urllib.error.HTTPError as e:
            payload = e.read().decode(errors="replace")[:2000]
            last_err = f"HTTP {e.code}: {payload}"
            if e.code in (400, 401, 403, 404):
                break  # not retryable
        except Exception as e:  # timeouts, conn resets, payload errors
            last_err = f"{type(e).__name__}: {e}"
            if "PIN VIOLATION" in str(e):
                break
        time.sleep(min(2 ** attempt * 5, 120))
    return {"request": body, "response": None, "latency_s": None,
            "error": last_err}


def usage_summary(result):
    """Pull the numbers that matter from a chat() result."""
    r = result.get("response") or {}
    u = r.get("usage") or {}
    d = u.get("completion_tokens_details") or {}
    ch = (r.get("choices") or [{}])[0]
    msg = ch.get("message") or {}
    return {
        "provider": r.get("provider"),
        "prompt_tokens": u.get("prompt_tokens"),
        "completion_tokens": u.get("completion_tokens"),
        "reasoning_tokens": d.get("reasoning_tokens"),
        "cost_usd": u.get("cost"),
        "finish_reason": ch.get("finish_reason"),
        "has_reasoning_field": bool(msg.get("reasoning")
                                    or msg.get("reasoning_content")),
        "content_len": len(msg.get("content") or ""),
    }


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", default="What is 17*23? Answer with the number only.")
    ap.add_argument("--effort", default="low",
                    choices=["off", "low", "medium", "xhigh"])
    ap.add_argument("--effort-mode", default="raw",
                    choices=["raw", "openrouter"])
    a = ap.parse_args()
    res = chat([{"role": "user", "content": a.prompt}], a.effort,
               a.effort_mode)
    print(json.dumps(usage_summary(res), indent=2))
    if res["error"]:
        print("ERROR:", res["error"])
    else:
        msg = res["response"]["choices"][0]["message"]
        print("content:", (msg.get("content") or "")[:300])
