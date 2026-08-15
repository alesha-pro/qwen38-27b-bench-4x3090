#!/usr/bin/env python3
"""Собирает все прогоны output/depth-*/bench.json в один файл результатов.

    python3 collect_results.py > output/RESULTS-Qwen3.8-27B.md

Пересобирает файл целиком каждый раз, поэтому его можно гонять после каждого
нового прогона и не думать про дописывание в конец.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "output"


def read_maybe_truncated(path: Path) -> list:
    """llama-bench пишет json потоком и не закрывает массив, если упал на
    очередной точке. 14.08 прогон на одной карте не смог создать контекст на
    глубине 131072, и восемь уже посчитанных строк лежали в файле без финальной
    скобки — а сборщик их молча выбрасывал. Дочиняем и говорим вслух."""
    text = path.read_text()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    cut = text.rfind("\n  }")
    if cut == -1:
        print(f"<!-- {path}: не удалось прочитать вообще -->")
        return []
    try:
        rows = json.loads(text[: cut + 4] + "\n]")
    except json.JSONDecodeError:
        print(f"<!-- {path}: не удалось починить -->")
        return []
    print(f"<!-- {path}: файл оборван, восстановлено {len(rows)} строк -->")
    return rows


def load_runs():
    runs = []
    for d in sorted(OUT.glob("depth-*")):
        j = d / "bench.json"
        if not j.exists() or j.stat().st_size == 0:
            continue
        rows = read_maybe_truncated(j)
        if not rows:
            continue
        m = re.match(r"depth-(.+?)-(\d+)gpu-(.+)", d.name)
        if not m:
            continue
        runs.append({
            "quant": m.group(1),
            "ngpu": int(m.group(2)),
            "stamp": m.group(3),
            "dir": d,
            "rows": rows,
        })
    return runs


def table(run):
    """Одна таблица: глубина × (prefill, decode)."""
    by_depth = {}
    for r in run["rows"]:
        d = r.get("n_depth", 0)
        kind = "prefill" if r["n_prompt"] else "decode"
        by_depth.setdefault(d, {})[kind] = (r["avg_ts"], r.get("stddev_ts", 0))

    depths = sorted(by_depth)
    base_pp = by_depth[depths[0]].get("prefill", (None,))[0]
    base_tg = by_depth[depths[0]].get("decode", (None,))[0]

    lines = ["| глубина | prefill tok/s | от глубины 0 | decode tok/s | от глубины 0 |",
             "|---|---|---|---|---|"]
    for d in depths:
        pp = by_depth[d].get("prefill")
        tg = by_depth[d].get("decode")
        pps = f"{pp[0]:.1f} ± {pp[1]:.1f}" if pp else "—"
        tgs = f"{tg[0]:.2f} ± {tg[1]:.2f}" if tg else "—"
        ppr = f"{100 * pp[0] / base_pp:.1f}%" if pp and base_pp else "—"
        tgr = f"{100 * tg[0] / base_tg:.1f}%" if tg and base_tg else "—"
        lines.append(f"| {d} | {pps} | {ppr} | {tgs} | {tgr} |")
    return "\n".join(lines)


def load_mtp_depth():
    """Прогоны bench_mtp_depth.sh: A/B по глубине через llama-server."""
    out = []
    for d in sorted(OUT.glob("mtpdepth-*")):
        m = re.match(r"mtpdepth-(.+?)-(\d+)gpu-(.+)", d.name)
        if not m:
            continue
        points = {}
        for f in d.glob("*-d*.json"):
            fm = re.match(r"(bez-mtp|s-mtp)-d(\d+)\.json", f.name)
            if not fm:
                continue
            try:
                lv = json.loads(f.read_text())["levels"][0]
            except Exception:
                continue
            points.setdefault(int(fm.group(2)), {})[fm.group(1)] = lv
        if points:
            out.append({"quant": m.group(1), "ngpu": int(m.group(2)), "dir": d, "points": points})
    return out


def load_mtp_single():
    """Прогоны bench_mtp.sh: A/B на одной глубине."""
    out = []
    for d in sorted(OUT.glob("mtp-*")):
        m = re.match(r"mtp-(.+?)-(\d+)gpu-(.+)", d.name)
        if not m:
            continue
        vals = {}
        for name in ("bez-mtp", "s-mtp"):
            f = d / f"{name}.json"
            if f.exists():
                try:
                    vals[name] = json.loads(f.read_text())["levels"][0]
                except Exception:
                    pass
        if len(vals) == 2:
            out.append({"quant": m.group(1), "ngpu": int(m.group(2)), "dir": d, "vals": vals})
    return out


def acceptance(log: Path) -> list:
    """Все записи о приёме черновика из лога сервера, по порядку запросов."""
    if not log.exists():
        return []
    rows = []
    for line in log.read_text(errors="replace").splitlines():
        m = re.search(r"draft acceptance = ([\d.]+) \(\s*(\d+) accepted /\s*(\d+) generated\), mean len =\s*([\d.]+)", line)
        if m:
            rows.append({
                "rate": float(m.group(1)),
                "accepted": int(m.group(2)),
                "generated": int(m.group(3)),
                "mean_len": float(m.group(4)),
            })
    return rows


def main():
    runs = load_runs()
    print("# Qwen3.8-27B: замеры на 4x RTX 3090, 14.08.2026\n")
    print("Релиз в 17:58:56 MSK (unsloth опередил сам Qwen на минуту), веса на риге")
    print("в 18:06:47 — восемь минут от публикации до диска.\n")

    if not runs:
        print("Пока ни одного законченного прогона.")
        return

    k = runs[0]["rows"][0]
    print("## Условия\n")
    print(f"- llama.cpp build {k.get('build_number')} (`{k.get('build_commit')}`), собран сегодня из master")
    print(f"- модель {k.get('model_n_params') / 1e9:.1f}B параметров, файл {k.get('model_size') / 1e9:.2f} GB")
    print(f"- архитектура в GGUF: `qwen35`, 65 блоков (64 рабочих + 1 MTP), контекст 262144")
    print(f"- flash attention: {'вкл' if k.get('flash_attn') else 'выкл'}, KV в {k.get('type_k')}/{k.get('type_v')}")
    print(f"- все слои на GPU (`-ngl {k.get('n_gpu_layers')}`), power limit 320 W")
    print(f"- prefill меряется промптом 4096 токенов, decode — генерацией 128 токенов, по 3 повтора")
    print("- параллельность не мерялась: по решению Алексея на llama.cpp меряем одиночный поток\n")

    for run in sorted(runs, key=lambda r: (r["quant"], r["ngpu"])):
        print(f"## {run['quant']}, {run['ngpu']} карт{'а' if run['ngpu'] == 1 else ''}\n")
        print(table(run))
        fail = run["dir"] / "failed_depth.txt"
        if fail.exists():
            print(f"\nНа глубине {fail.read_text().strip()} контекст создать не удалось — "
                  f"весов и кэша уже не хватает.")
        print(f"\nсырьё: `{run['dir'].relative_to(ROOT)}`\n")

    maxctx = []
    for d in sorted(OUT.glob("maxctx-*")):
        f = d / "max_ctx.txt"
        if f.exists():
            maxctx.append((d.name.replace("maxctx-", "").rsplit("-2026", 1)[0], int(f.read_text().strip()), d))
    if maxctx:
        print("# Максимальный контекст на ОДНОЙ карте\n")
        print("Двоичный поиск по `--ctx-size` с шагом 1024, один слот, все слои на GPU,")
        print("flash attention включён, KV в f16. Успех — сервер ответил на /health.\n")
        # размер файла берём из прогонов llama-bench, там он записан точно
        sizes = {}
        for r in runs:
            sizes.setdefault(r["quant"], r["rows"][0].get("model_size"))

        print("| квант | вес файла | максимум токенов | следующий шаг |")
        print("|---|---|---|---|")
        rows_mc = []
        for name, val, d in maxctx:
            sz = sizes.get(name)
            szs = f"{sz / 1e9:.2f} GB" if sz else "—"
            print(f"| {name} | {szs} | **{val}** | {val + 1024} падает |")
            if sz:
                rows_mc.append((name, sz, val))
        print()

        # Цена одного токена контекста: сколько байт VRAM он забирает. Считаем по
        # РАЗНОСТЯМ между квантами — так уходят все постоянные накладные расходы
        # (буферы, контекст CUDA, сам движок), и остаётся чистая цена кэша.
        rows_mc.sort(key=lambda x: x[1])
        if len(rows_mc) >= 2:
            print("**Сколько стоит один токен контекста.** Считаем по разностям между")
            print("квантами: постоянные накладные расходы одинаковы у всех и при вычитании")
            print("уходят, остаётся чистая цена кэша.\n")
            print("| переход | лишних весов | потеряно токенов | байт на токен |")
            print("|---|---|---|---|")
            per = []
            for (n1, s1, c1), (n2, s2, c2) in zip(rows_mc, rows_mc[1:]):
                dw, dc = s2 - s1, c1 - c2
                if dc <= 0:
                    continue
                b = dw / dc
                per.append(b)
                print(f"| {n1} → {n2} | {dw / 1e9:.2f} GB | {dc} | **{b:,.0f}** |")
            if len(per) >= 2:
                spread = 100 * (max(per) / min(per) - 1)
                print(f"\nДва независимых перехода дали {per[0]:,.0f} и {per[1]:,.0f} байт на")
                print(f"токен, расхождение {spread:.1f}%. Значит память под контекст растёт")
                print("линейно и предсказуемо.\n")
            print("Сходится с раскладкой слоёв из README: настоящее внимание только на")
            print("каждом четвёртом слое, то есть на 16 из 64. На слой выходит")
            print("2 × 4 KV-головы × 256 размер головы × 2 байта = 4096 байт, на все")
            print("шестнадцать 65536 байт на токен. Померенное чуть выше расчётного,")
            print("разницу, вероятно, добирают буферы под вычисления, которые тоже растут")
            print("с контекстом. Проверкой это не подтверждено, поэтому догадка.\n")
            print("У обычного трансформера со вниманием на всех 64 слоях тот же токен")
            print("стоил бы вчетверо дороже.\n")

        for _, _, d in maxctx:
            print(f"сырьё: `{d.relative_to(ROOT)}`\n")

    singles = load_mtp_single()
    depths = load_mtp_depth()
    if not (singles or depths):
        return

    print("# Спекулятивный декодинг (MTP)\n")
    print("MTP-голова (`blk.64.nextn.*`) лежит внутри самого кванта, отдельная")
    print("драфт-модель не нужна. llama.cpp грузит эти тензоры только по флагу")
    print("`--spec-type draft-mtp`; без него они выбрасываются с предупреждением")
    print("`unused tensor ... ignoring`, и это легко принять за отсутствие поддержки.\n")
    print("**Замеры ниже сняты через llama-server, а не llama-bench** (llama-bench")
    print("спекулятивный декодинг не умеет), поэтому prefill здесь означает другое:")
    print("это время до первого токена на холодном промпте заданной длины, тогда как")
    print("в таблицах выше — обработка новых 4096 токенов поверх уже набранного")
    print("контекста. Складывать эти числа в одну колонку нельзя.\n")

    for s in singles:
        a = s["vals"]["bez-mtp"]["decode_tok_s_median"]
        b = s["vals"]["s-mtp"]["decode_tok_s_median"]
        acc = acceptance(s["dir"] / "server-s-mtp.log")
        print(f"## {s['quant']}, {s['ngpu']} карта, короткий промпт\n")
        print("| | decode tok/s |")
        print("|---|---|")
        print(f"| без MTP | {a} |")
        print(f"| с MTP | {b} |")
        print(f"| выигрыш | **{100 * (b / a - 1):+.1f}%** |")
        if acc:
            last = acc[-1]
            print(f"\nПриём черновика на зачётном запросе: {last['rate']:.3f} "
                  f"({last['accepted']} принято / {last['generated']} предложено), "
                  f"средняя длина принятой серии {last['mean_len']:.2f}.")
        print(f"\nсырьё: `{s['dir'].relative_to(ROOT)}`\n")

    for r in depths:
        print(f"## {r['quant']}, {r['ngpu']} карта, MTP по глубине контекста\n")
        print("| глубина | без MTP | с MTP | выигрыш |")
        print("|---|---|---|---|")
        gains = []
        for d in sorted(r["points"]):
            p = r["points"][d]
            a = (p.get("bez-mtp") or {}).get("decode_tok_s_median")
            b = (p.get("s-mtp") or {}).get("decode_tok_s_median")
            g = f"**{100 * (b / a - 1):+.1f}%**" if a and b else "—"
            if a and b:
                gains.append(100 * (b / a - 1))
            print(f"| {d} | {a if a else '—'} | {b if b else '—'} | {g} |")
        if len(gains) >= 3:
            print(f"\nВыигрыш гуляет от {min(gains):+.1f}% до {max(gains):+.1f}% и НЕ")
            print("выстраивается по глубине. Причина в приёме черновика: при")
            print("`temperature 0.7` каждый прогон сочиняет свой текст, и насколько он")
            print("предсказуем, настолько MTP и экономит. Одного запроса на точку для")
            print("такого вопроса мало — эффект глубины тонет в разбросе сэмплинга.")
            print("Чтобы его увидеть, нужен жадный декодинг или несколько запросов на точку.")
        print(f"\nсырьё: `{r['dir'].relative_to(ROOT)}`\n")


if __name__ == "__main__":
    main()
