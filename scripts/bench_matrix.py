#!/usr/bin/env python3
"""Матрица замеров против уже поднятого OpenAI-совместимого сервера.

Повторяет условия baseline Qwen3.6-27B (bench-db, 2026-07-26): single-stream
плюс aggregate на 1/4/16/32 потоках, стриминг, TTFT по первому чанку.

    python3 bench_matrix.py --port 18000 --model bench --out ~/benchmarks/qwen38/run.json
"""

from __future__ import annotations

import argparse
import json
import statistics
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

PROMPT = (
    "Explain how tensor parallelism splits a transformer layer across four GPUs, "
    "and why the all-reduce placement matters for latency. Be concrete."
)

# Наполнитель для замера prefill. Проза, а не повтор одного слова: у токенизатора
# на мусоре другое соотношение символов к токенам, и длина промпта поплывёт.
FILLER = (
    "The scheduler walks the ready queue and assigns each pending sequence to a "
    "free slot, then the attention kernel reads the key value cache block by "
    "block while the router picks experts for the current token. Memory traffic "
    "dominates at low batch sizes and compute dominates once the batch grows. "
)

# llama-server до определённых сборок отвечает 400 на chat_template_kwargs.
# Ставится в False автоматически на прогреве, см. main().
USE_THINKING_KWARG = True


def make_prompt(idx: int, prompt_tokens: int, salt: str = "", chars_per_token: float = 4.0) -> str:
    """Промпт обязан быть уникальным В ПРЕДЕЛАХ ВСЕГО ПРОГОНА, а не только уровня.

    Найдено на холостом прогоне 14.08: idx начинается с нуля на каждом уровне
    конкурентности, поэтому запрос 0 на c=2 был байт в байт равен запросу на c=1,
    попадал в prefix cache сервера и давал TTFT 116 мс вместо 2.7 с. Медиана
    prefill улетала в 3432 tok/s на модели, которая физически даёт ~300.
    Отсюда salt: в него кладём уровень конкурентности и метку запуска.
    """
    if prompt_tokens <= 0:
        return f"{PROMPT} (variant {idx}, run {salt})"
    need_chars = int(prompt_tokens * chars_per_token)
    head = f"Request {idx} of run {salt}, nonce {idx * 7919 + len(salt)}. "
    body = FILLER * (need_chars // len(FILLER) + 1)
    return head + body[:need_chars] + "\n\nSummarize the text above in one sentence."


def one_request(url: str, model: str, prompt: str, max_tokens: int, out: list, idx: int) -> None:
    try:
        _one_request(url, model, prompt, max_tokens, out, idx)
    except Exception as exc:  # ошибка потока иначе теряется молча
        detail = ""
        if isinstance(exc, urllib.error.HTTPError):
            try:
                detail = exc.read().decode()[:300]
            except Exception:
                pass
        out[idx] = {"error": f"{exc!r} {detail}".strip()}


def _one_request(url: str, model: str, prompt: str, max_tokens: int, out: list, idx: int) -> None:
    payload_obj = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "stream": True,
        "stream_options": {"include_usage": True},
    }
    if USE_THINKING_KWARG:
        payload_obj["chat_template_kwargs"] = {"enable_thinking": False}
    body = json.dumps(payload_obj).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    t0 = time.time()
    ttft = None
    ntok = 0
    ptok = 0
    with urllib.request.urlopen(req, timeout=1800) as resp:
        for raw in resp:
            line = raw.decode().strip()
            if not line.startswith("data:"):
                continue
            payload = line[5:].strip()
            if payload == "[DONE]":
                break
            chunk = json.loads(payload)
            if chunk.get("usage"):
                ntok = chunk["usage"]["completion_tokens"]
                ptok = chunk["usage"].get("prompt_tokens", 0)
            if not chunk.get("choices"):
                continue
            delta = chunk["choices"][0].get("delta", {})
            text = delta.get("content") or delta.get("reasoning_content") or ""
            if text and ttft is None:
                ttft = time.time() - t0
    total = time.time() - t0
    effective_ttft = ttft or total
    out[idx] = {
        "ttft_s": effective_ttft,
        "total_s": total,
        "tokens": ntok,
        "prompt_tokens": ptok,
        # Absolute timestamps let the depth runner distinguish end-to-end
        # throughput (which includes a long prefill) from the shared decode
        # window after the first generated token has appeared.
        "started_at": t0,
        "first_token_at": t0 + effective_ttft,
        "finished_at": t0 + total,
    }


def run_level(
    url: str,
    model: str,
    conc: int,
    max_tokens: int,
    prompt_tokens: int = 0,
    salt: str = "",
    chars_per_token: float = 4.0,
) -> dict:
    out: list = [None] * conc
    level_salt = f"{salt}c{conc}"
    threads = [
        threading.Thread(
            target=one_request,
            args=(url, model, make_prompt(i, prompt_tokens, level_salt, chars_per_token), max_tokens, out, i),
        )
        for i in range(conc)
    ]
    t0 = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    wall = time.time() - t0

    errors = [r["error"] for r in out if r and "error" in r]
    ok = [r for r in out if r and "error" not in r]
    tokens = sum(r["tokens"] for r in ok)
    ttfts = sorted(r["ttft_s"] for r in ok)
    # decode = токены после первого, поделённые на время после TTFT
    decodes = [
        (r["tokens"] - 1) / (r["total_s"] - r["ttft_s"])
        for r in ok
        if r["tokens"] > 1 and r["total_s"] > r["ttft_s"]
    ]
    # prefill: столько-то токенов промпта переварено за время до первого токена.
    # На коротком промпте это в основном накладные расходы, поэтому число
    # осмысленно только при --prompt-tokens в тысячах.
    prompt_toks = [r.get("prompt_tokens", 0) for r in ok]
    prefills = [
        r["prompt_tokens"] / r["ttft_s"]
        for r in ok
        if r.get("prompt_tokens") and r["ttft_s"] > 0
    ]
    row = {
        "concurrency": conc,
        "requests_ok": len(ok),
        "errors": errors[:3],
        "wall_s": round(wall, 2),
        "total_tokens": tokens,
        "aggregate_tok_s": round(tokens / wall, 2) if wall else None,
        "decode_tok_s_median": round(statistics.median(decodes), 2) if decodes else None,
        "ttft_p50_ms": round(statistics.median(ttfts) * 1000, 1) if ttfts else None,
        # Было ttft_p99_ms по формуле int(n*0.99)-1. На n=2 она возвращала
        # ttfts[0], то есть МИНИМУМ: в холостом прогоне 14.08 вышло p99=116 мс
        # при p50=1414 мс. По 8 запросам девяносто девятого процентиля не бывает,
        # поэтому честнее отдавать максимум и так его и называть.
        "ttft_max_ms": round(max(ttfts) * 1000, 1) if ttfts else None,
    }
    decode_window_rows = [
        r
        for r in ok
        if r["tokens"] > 1
        and r.get("first_token_at") is not None
        and r.get("finished_at") is not None
        and r["finished_at"] > r["first_token_at"]
    ]
    if decode_window_rows:
        decode_window_s = max(r["finished_at"] for r in decode_window_rows) - min(
            r["first_token_at"] for r in decode_window_rows
        )
        decode_tokens_after_first = sum(r["tokens"] - 1 for r in decode_window_rows)
        row["decode_window_s"] = round(decode_window_s, 3)
        row["decode_tokens_after_first"] = decode_tokens_after_first
        row["aggregate_decode_window_tok_s"] = (
            round(decode_tokens_after_first / decode_window_s, 2)
            if decode_window_s > 0
            else None
        )
        # This is the sum of each request's steady decode rate. It is useful
        # alongside the conservative shared-window rate when long prefills make
        # the requests enter decode at different moments.
        row["aggregate_active_decode_rate_sum"] = round(sum(decodes), 2)
    if prompt_toks and max(prompt_toks) > 0:
        row["prompt_tokens_median"] = int(statistics.median(prompt_toks))
        row["prefill_tok_s_median"] = round(statistics.median(prefills), 1) if prefills else None
        # агрегат: все запросы стартуют вместе, значит весь промпт переварен
        # к моменту самого позднего первого токена
        row["prefill_tok_s_aggregate"] = (
            round(sum(prompt_toks) / max(ttfts), 1) if ttfts and max(ttfts) > 0 else None
        )
    return row


def main() -> int:
    global USE_THINKING_KWARG
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=18000)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--model", default="bench")
    ap.add_argument("--levels", default="1,2,4,8")
    ap.add_argument("--max-tokens", type=int, default=256)
    ap.add_argument(
        "--prompt-tokens",
        type=int,
        default=0,
        help="0 — короткий промпт как в baseline (мерим decode). >0 — длинный промпт, мерим prefill.",
    )
    ap.add_argument("--out", default=None)
    ap.add_argument("--label", default="")
    args = ap.parse_args()

    url = f"http://{args.host}:{args.port}/v1/chat/completions"
    levels = [int(x) for x in args.levels.split(",")]

    print(f"warmup → {url}")
    warm: list = [None]
    one_request(url, args.model, "hi", 8, warm, 0)
    # llama-server старых сборок не знает chat_template_kwargs и отвечает 400.
    # Молча уронить весь прогон из-за этого нельзя — снимаем поле и пробуем ещё раз.
    if warm[0] and "error" in warm[0] and USE_THINKING_KWARG:
        print(f"прогрев не прошёл: {warm[0]['error'][:200]}")
        print("повтор без chat_template_kwargs (сервер, похоже, его не знает)")
        USE_THINKING_KWARG = False
        one_request(url, args.model, "hi", 8, warm, 0)
    if warm[0] and "error" in warm[0]:
        print(f"ПРОГРЕВ ПРОВАЛЕН: {warm[0]['error'][:500]}")
        return 1

    # Метка прогона: попадает в каждый промпт, чтобы ни один запрос не совпал
    # с запросом соседнего уровня и не сел на prefix cache сервера.
    salt = f"{int(time.time() * 1000) % 100000000:08d}-"

    # Символов на токен считаем по факту, а не по прикидке: у разных
    # токенизаторов соотношение разное, и «prefill на 4096 токенах» должен
    # быть на 4096, а не на 767, как вышло на холостом прогоне с оценкой 4.0.
    chars_per_token = 4.0
    if args.prompt_tokens > 0:
        probe: list = [None]
        one_request(
            url, args.model, make_prompt(999, args.prompt_tokens, salt + "cal", chars_per_token), 8, probe, 0
        )
        got = (probe[0] or {}).get("prompt_tokens") or 0
        if got > 0:
            chars_per_token = round(chars_per_token * args.prompt_tokens / got, 3)
            print(f"калибровка промпта: запрошено {args.prompt_tokens}, вышло {got} → {chars_per_token} симв/токен")
        else:
            print("калибровка не удалась, беру 4.0 симв/токен; длину смотреть в prompt_tokens_median")

    result = {
        "label": args.label,
        "when": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "url": url,
        "model": args.model,
        "max_tokens": args.max_tokens,
        "prompt_tokens_requested": args.prompt_tokens,
        "chars_per_token": chars_per_token,
        "thinking_kwarg": USE_THINKING_KWARG,
        "run_salt": salt,
        "levels": [],
    }

    for conc in levels:
        print(f"--- concurrency {conc}")
        row = run_level(url, args.model, conc, args.max_tokens, args.prompt_tokens, salt, chars_per_token)
        print(json.dumps(row, ensure_ascii=False))
        result["levels"].append(row)

    if args.out:
        with open(args.out, "w") as fh:
            json.dump(result, fh, indent=2, ensure_ascii=False)
        print(f"\nсохранено: {args.out}")

    print("\n=== сводка (сравнивать с Qwen3.6-27B-FP8 TP=4 220W: 61.6 decode, 505 мс TTFT, 281 tok/s @c32) ===")
    for row in result["levels"]:
        if not row["requests_ok"]:
            print(f"c={row['concurrency']:>3}  ПРОВАЛ: {row['errors']}")
            continue
        line = (
            f"c={row['concurrency']:>3}  agg={row['aggregate_tok_s']:>8}  "
            f"decode_med={row['decode_tok_s_median']}  ttft_p50={row['ttft_p50_ms']} мс"
        )
        if row.get("prefill_tok_s_aggregate"):
            line += (
                f"  | prefill {row['prompt_tokens_median']} ток: "
                f"med={row['prefill_tok_s_median']} agg={row['prefill_tok_s_aggregate']} tok/s"
            )
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
