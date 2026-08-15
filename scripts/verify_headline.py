#!/usr/bin/env python3
"""Перепроверка хедлайновой ячейки: vLLM NVFP4 TP4/FP8KV/MTP2.

Ячейка 254K показала 84.26 tok/s, но на 49 токенах decode за 0.58 c
(модель встала на EOS на 50-м токене из 128). Здесь: тот же сервер,
те же chat-запросы при temp 0.7, но max_tokens=512 + ignore_eos, по 3
повтора на глубинах 253952 и 8192 (точка 8K 57.18 тоже выглядела шумной).
"""
import json, subprocess, sys, time, urllib.request

sys.path.insert(0, "$BENCH_ROOT")
import bench_matrix

PORT = 18081
URL = f"http://127.0.0.1:{PORT}"
CMD = json.load(open("$BENCH_ROOT/output/"
    "vllm-depth-autonomous-qwen38-nvfp4/configs/tp4-fp8-mtp2/launch-attempt-13.json"))["command"]

def tokenize_count(prompt):
    body = json.dumps({"model": "bench", "prompt": prompt}).encode()
    req = urllib.request.Request(f"{URL}/tokenize", body,
                                 {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)["count"]

def prompt_for_depth(depth, salt):
    cpt = 5.5649
    for _ in range(6):
        p = bench_matrix.make_prompt(0, depth, salt=salt, chars_per_token=cpt)
        n = tokenize_count(p)
        if abs(n - depth) <= 64:
            return p, n
        cpt *= depth / max(n, 1)
    return p, n

def measure(prompt, max_tokens=512):
    body = json.dumps({
        "model": "bench",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens, "temperature": 0.7,
        "ignore_eos": True, "stream": True,
        "stream_options": {"include_usage": True},
    }).encode()
    req = urllib.request.Request(f"{URL}/v1/chat/completions", body,
                                 {"Content-Type": "application/json"})
    t0 = time.monotonic(); t_first = None; t_last = None; completion = None
    with urllib.request.urlopen(req, timeout=1200) as r:
        for raw in r:
            line = raw.decode("utf-8", "ignore").strip()
            if not line.startswith("data:"):
                continue
            data = line[5:].strip()
            if data == "[DONE]":
                break
            chunk = json.loads(data)
            if chunk.get("usage"):
                completion = chunk["usage"].get("completion_tokens")
            if chunk.get("choices"):
                d = chunk["choices"][0].get("delta", {})
                if d.get("content"):
                    now = time.monotonic()
                    if t_first is None:
                        t_first = now
                    t_last = now
    ttft = t_first - t0
    window = t_last - t_first
    toks = (completion or 0) - 1
    return {"ttft_s": round(ttft, 1), "decode_window_s": round(window, 3),
            "decode_tokens": toks,
            "decode_tok_s": round(toks / window, 2) if window > 0 else None}

def main():
    print("== запускаю сервер:", " ".join(CMD[:4]), "... (TP4/FP8KV/MTP2)")
    srv = subprocess.Popen(CMD, stdout=open("/tmp/verify-server.log", "w"),
                           stderr=subprocess.STDOUT,
                           env={**__import__("os").environ,
                                "CUDA_VISIBLE_DEVICES": "0,1,2,3",
                                "CUDA_HOME": "$ENGINES/vllm-cross-kv-env/lib/python3.12/site-packages/nvidia/cu13"})
    try:
        for i in range(240):
            time.sleep(10)
            try:
                urllib.request.urlopen(f"{URL}/health", timeout=5)
                break
            except Exception:
                if srv.poll() is not None:
                    print("сервер умер, хвост лога:")
                    print(open("/tmp/verify-server.log").read()[-3000:])
                    sys.exit(1)
        else:
            print("сервер не поднялся за 40 мин"); sys.exit(1)
        print("== сервер жив, прогреваю")
        measure(bench_matrix.make_prompt(0, 256, salt="warmup"), max_tokens=32)

        for depth in (8192, 253952):
            print(f"== глубина {depth}, 3 повтора, 512 токенов, ignore_eos")
            for i in range(3):
                p, n = prompt_for_depth(depth, salt=f"verify-{depth}-{i}")
                r = measure(p)
                print(f"   run {i}: prompt={n} ttft={r['ttft_s']}s "
                      f"decode={r['decode_tok_s']} tok/s "
                      f"({r['decode_tokens']} ток за {r['decode_window_s']}s)",
                      flush=True)
    finally:
        srv.terminate()
        time.sleep(10)
        srv.kill()
    print("== готово")

main()
