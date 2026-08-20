#!/usr/bin/env python3
"""Transparent OpenAI endpoint proxy with lossless per-request JSONL telemetry."""

from __future__ import annotations

import argparse
import http.client
import json
import os
import re
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

SESSION_PATH = re.compile(r"^/session/([^/]+)(/.*)$")
HOP_HEADERS = {
    "connection",
    "content-encoding",
    "content-length",
    "host",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_json(body: bytes):
    try:
        return json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None


def scenario_policy_key(scenario: str | None) -> str | None:
    if not scenario:
        return None
    parts = scenario.split("/")
    return "/".join(parts[:2]) if len(parts) >= 2 else scenario


def reasoning_policy(request: dict) -> dict | None:
    """Extract an explicit reasoning policy from a canonical runner request."""
    kwargs = request.get("chat_template_kwargs")
    kwargs = kwargs if isinstance(kwargs, dict) else {}
    has_top_effort = "reasoning_effort" in request
    controlled_kwargs = {
        key: kwargs[key] for key in ("enable_thinking", "reasoning_effort") if key in kwargs
    }
    if not has_top_effort and not controlled_kwargs:
        return None
    effort = request.get("reasoning_effort") if has_top_effort else controlled_kwargs.get("reasoning_effort")
    enabled = (
        controlled_kwargs.get("enable_thinking") is True
        or str(effort).lower() in {"low", "medium", "high", "xhigh"}
    )
    return {
        "has_top_effort": has_top_effort,
        "top_effort": request.get("reasoning_effort"),
        "template_kwargs": controlled_kwargs,
        # The canonical thinking request deliberately has no output cap. Every
        # auxiliary call inside the same scenario must inherit that contract.
        "strip_output_caps": enabled and not any(
            key in request for key in ("max_tokens", "max_completion_tokens")
        ),
    }


def apply_reasoning_policy(request: dict, policy: dict) -> tuple[dict, list[str]]:
    forwarded = dict(request)
    rewrites: list[str] = []
    if policy.get("has_top_effort") and forwarded.get("reasoning_effort") != policy.get("top_effort"):
        forwarded["reasoning_effort"] = policy.get("top_effort")
        rewrites.append("reasoning_effort")
    controlled = policy.get("template_kwargs") or {}
    if controlled:
        kwargs = forwarded.get("chat_template_kwargs")
        kwargs = dict(kwargs) if isinstance(kwargs, dict) else {}
        changed = False
        for key, value in controlled.items():
            if kwargs.get(key) != value:
                kwargs[key] = value
                changed = True
        if changed or not isinstance(forwarded.get("chat_template_kwargs"), dict):
            forwarded["chat_template_kwargs"] = kwargs
            rewrites.append("chat_template_kwargs")
    if policy.get("strip_output_caps"):
        for key in ("max_tokens", "max_completion_tokens"):
            if key in forwarded:
                forwarded.pop(key)
                rewrites.append(f"remove_{key}")
    return forwarded, rewrites


def policy_signature(policy: dict) -> tuple:
    return (
        policy.get("has_top_effort"),
        str(policy.get("top_effort")),
        tuple(sorted((policy.get("template_kwargs") or {}).items())),
    )


def response_capture(value, raw_body: bytes) -> tuple[dict, dict]:
    if not isinstance(value, dict):
        reasoning_parts: list[str] = []
        answer_parts: list[str] = []
        tool_fragments: list[object] = []
        finish_reasons: list[str] = []
        usage = None
        chunk_count = 0
        for line in raw_body.decode("utf-8", errors="replace").splitlines():
            if not line.startswith("data:"):
                continue
            payload = line[5:].strip()
            if not payload or payload == "[DONE]":
                continue
            try:
                chunk = json.loads(payload)
            except json.JSONDecodeError:
                continue
            chunk_count += 1
            if isinstance(chunk.get("usage"), dict):
                usage = chunk["usage"]
            choices = chunk.get("choices")
            choice = choices[0] if isinstance(choices, list) and choices and isinstance(choices[0], dict) else {}
            delta = choice.get("delta") if isinstance(choice.get("delta"), dict) else {}
            reasoning = delta.get("reasoning_content")
            if reasoning is None:
                reasoning = delta.get("reasoning")
            if isinstance(reasoning, str):
                reasoning_parts.append(reasoning)
            if isinstance(delta.get("content"), str):
                answer_parts.append(delta["content"])
            if isinstance(delta.get("tool_calls"), list):
                tool_fragments.extend(delta["tool_calls"])
            if choice.get("finish_reason") is not None:
                finish_reasons.append(str(choice["finish_reason"]))
        extracted = {
            "reasoning_content": "".join(reasoning_parts),
            "content": "".join(answer_parts),
            "tool_call_fragments": tool_fragments,
        }
        return {
            "stream": True,
            "stream_chunk_count": chunk_count,
            "usage": usage,
            "finish_reason": finish_reasons[-1] if finish_reasons else None,
            "reasoning_chars": len(extracted["reasoning_content"]),
            "answer_chars": len(extracted["content"]),
            "tool_call_fragment_count": len(tool_fragments),
        }, extracted
    choices = value.get("choices")
    choice = choices[0] if isinstance(choices, list) and choices and isinstance(choices[0], dict) else {}
    message = choice.get("message") if isinstance(choice.get("message"), dict) else {}
    reasoning = message.get("reasoning_content")
    if reasoning is None:
        reasoning = message.get("reasoning")
    content = message.get("content")
    tool_calls = message.get("tool_calls")
    extracted = {
        "reasoning_content": reasoning if isinstance(reasoning, str) else "",
        "content": content if isinstance(content, str) else "",
        "tool_calls": tool_calls if isinstance(tool_calls, list) else [],
    }
    return {
        "stream": False,
        "usage": value.get("usage"),
        "finish_reason": choice.get("finish_reason"),
        "reasoning_chars": len(reasoning) if isinstance(reasoning, str) else 0,
        "answer_chars": len(content) if isinstance(content, str) else 0,
        "tool_call_count": len(tool_calls) if isinstance(tool_calls, list) else 0,
    }, extracted


class TelemetryServer(ThreadingHTTPServer):
    def __init__(self, address, handler, *, target: str, log_path: Path):
        super().__init__(address, handler)
        parsed = urlsplit(target)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError(f"invalid target: {target}")
        self.target_scheme = parsed.scheme
        self.target_host = parsed.hostname
        self.target_port = parsed.port or (443 if parsed.scheme == "https" else 80)
        self.target_prefix = parsed.path.rstrip("/")
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.log_lock = threading.Lock()
        self.policy_lock = threading.Lock()
        self.reasoning_policies: dict[str, dict] = {}

    def enforce_reasoning_policy(self, scenario: str | None, request: dict) -> tuple[dict, list[str]]:
        key = scenario_policy_key(scenario)
        if key is None:
            return request, []
        explicit = reasoning_policy(request)
        with self.policy_lock:
            existing = self.reasoning_policies.get(key)
            # A changed explicit control signature marks the next effort arm.
            # Within an arm, auxiliary clients may repeat the same controls but
            # must not weaken the canonical no-cap contract.
            if explicit is not None and (
                existing is None or policy_signature(explicit) != policy_signature(existing)
            ):
                self.reasoning_policies[key] = explicit
                existing = explicit
        return apply_reasoning_policy(request, existing) if existing is not None else (request, [])

    def write_record(self, record: dict) -> None:
        payload = json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"
        with self.log_lock:
            fd = os.open(self.log_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
            try:
                os.write(fd, payload.encode("utf-8"))
                os.fsync(fd)
            finally:
                os.close(fd)


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server: TelemetryServer

    def log_message(self, fmt: str, *args) -> None:
        print(f"[telemetry-proxy] {self.address_string()} {fmt % args}", flush=True)

    def do_GET(self) -> None:
        self._forward()

    def do_POST(self) -> None:
        self._forward()

    def _forward(self) -> None:
        content_length = int(self.headers.get("Content-Length", "0") or 0)
        request_body = self.rfile.read(content_length) if content_length else b""
        request_json = parse_json(request_body)
        incoming_path = self.path
        scenario = self.headers.get("X-Benchlocal-Scenario")
        session_match = SESSION_PATH.match(incoming_path)
        if session_match:
            scenario = unquote(session_match.group(1))
            incoming_path = session_match.group(2)
        incoming_request_json = request_json
        request_rewrites: list[str] = []
        if (
            isinstance(request_json, dict)
            and incoming_path.endswith("/chat/completions")
        ):
            request_json, request_rewrites = self.server.enforce_reasoning_policy(
                scenario, request_json
            )
            request_body = json.dumps(
                request_json, ensure_ascii=False, separators=(",", ":")
            ).encode("utf-8")
        target_path = f"{self.server.target_prefix}{incoming_path}"
        started_wall = utc_now()
        started = time.perf_counter()
        headers_at = None
        status = 502
        response_headers = []
        response_body = b""
        error = None
        try:
            connection_class = (
                http.client.HTTPSConnection
                if self.server.target_scheme == "https"
                else http.client.HTTPConnection
            )
            connection = connection_class(
                self.server.target_host,
                self.server.target_port,
                timeout=None,
            )
            forward_headers = {
                key: value
                for key, value in self.headers.items()
                if key.lower() not in HOP_HEADERS
            }
            forward_headers["Content-Length"] = str(len(request_body))
            connection.request(self.command, target_path, body=request_body, headers=forward_headers)
            upstream = connection.getresponse()
            headers_at = time.perf_counter()
            status = upstream.status
            response_headers = [
                (key, value)
                for key, value in upstream.getheaders()
                if key.lower() not in HOP_HEADERS
            ]
            response_body = upstream.read()
            connection.close()
        except Exception as exc:  # noqa: BLE001 - proxy must preserve evidence
            error = f"{type(exc).__name__}: {exc}"
            response_body = json.dumps({"error": {"message": error}}).encode("utf-8")
            response_headers = [("Content-Type", "application/json")]
        finished = time.perf_counter()
        response_json = parse_json(response_body)
        response_summary, response_extracted = response_capture(response_json, response_body)
        request_effort = request_json.get("reasoning_effort") if isinstance(request_json, dict) else None
        template_kwargs = request_json.get("chat_template_kwargs") if isinstance(request_json, dict) else None
        self.server.write_record({
            "schema_version": 2,
            "started_at": started_wall,
            "scenario": scenario,
            "attempt": self.headers.get("X-Benchlocal-Attempt"),
            "method": self.command,
            "incoming_path": self.path,
            "target_path": target_path,
            "status_code": status,
            "duration_seconds": finished - started,
            "response_headers_seconds": (
                headers_at - started if headers_at is not None else None
            ),
            "request_reasoning_effort": request_effort,
            "request_chat_template_kwargs": template_kwargs,
            "request_has_max_tokens": (
                "max_tokens" in request_json if isinstance(request_json, dict) else None
            ),
            "request_max_tokens": request_json.get("max_tokens") if isinstance(request_json, dict) else None,
            "request_rewrites": request_rewrites,
            "request_incoming": incoming_request_json if incoming_request_json is not None else request_body.decode("utf-8", errors="replace"),
            "request": request_json if request_json is not None else request_body.decode("utf-8", errors="replace"),
            "response_summary": response_summary,
            "response_extracted": response_extracted,
            "response": response_json if response_json is not None else response_body.decode("utf-8", errors="replace"),
            "error": error,
        })

        self.send_response(status)
        for key, value in response_headers:
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(response_body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(response_body)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--log", type=Path, required=True)
    args = parser.parse_args()
    server = TelemetryServer(
        (args.host, args.port),
        Handler,
        target=args.target,
        log_path=args.log,
    )
    print(
        f"[telemetry-proxy] listening on {args.host}:{args.port} -> {args.target}; "
        f"log={args.log}",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
