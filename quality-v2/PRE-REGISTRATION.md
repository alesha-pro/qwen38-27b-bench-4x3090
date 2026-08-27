# Local Quant Quality Benchmark v2

Status: **сьют заморожен 23.08.2026** — 100 задач, эталон BF16 снят на всех
четырёх режимах. Состав, калибровка, находки и расходы:
[`llm-bench/results/quant-bench-v2-calibration-2026-08-23/`](../results/quant-bench-v2-calibration-2026-08-23/README.md).
Дальше — канарейка против рига и прогон квантов.

## Решения Алексея, 2026-08-22 (средний вариант, приоритет над текстом ниже)

Обсуждение с Claude 22.08. Где этот блок противоречит остальному документу,
действует этот блок.

1. **Эталон BF16 через OpenRouter, не на риге.** Единственный bf16-эндпоинт
   `qwen/qwen3.8-27b` — провайдер **AkashML** ($0.45/$3.20 за 1M, ctx 262K,
   max output 131K, uptime 99.97%). Остальные провайдеры отдают fp8, поэтому
   пин обязателен: `provider: {"order": ["AkashML"], "allow_fallbacks": false}`
   + `quantizations: ["bf16"]`. Без пина эталон молча превратится в FP8.
   Оценка стоимости всего эталона (калибровка + финал 4 efforts): ~$25,
   с запасом до $50. Расчёт от реальной телеметрии первой кампании
   (FP8, 8 армов: 3.5M in / 4.2M out).
2. **Канарейка перед доверием к API**: 15-20 задач на AkashML против разового
   BF16 TP4 на риге, pass rate должен сойтись. Проверить, что
   off/low/medium/xhigh реально доезжают до модели (по reasoning-токенам в
   usage). После этого риг для эталона не нужен.
3. **Сэмплинг — официальная карточка Qwen3.8** (не 0.6, как у прошлых Qwen):
   thinking-армы `temperature=1.0, top_p=0.95, top_k=20, min_p=0,
   presence_penalty=0, repetition_penalty=1.0`; off-арм `temperature=0.7,
   top_p=0.80, top_k=20, presence_penalty=1.5`. Идентично для BF16 и всех
   квантов. Из-за temp=1.0 калибровка ОБЯЗАТЕЛЬНО включает 3 повтора xhigh
   на дев-пуле, чтобы измерить дисперсию и знать порог шума.
4. **Скоуп первого релиза срезан**: Agent Deep (DeepSWE/Terminal-Bench/
   MCPMark/Toolathlon/SWE-rebench) целиком отложен на второй этап; LiveBench
   выкинут; LongBench Pro (long context) отложен. Первый релиз = Quant Core
   (Reasoning Gym ~40 + MathArena ~16 + IFBench ~20) + Tool Calling
   (BFCL ~24), итого ~100 замороженных задач. Дев-пул ~250
   (RG 120 = 10 семейств x 12, MathArena 20, IFBench 60, BFCL 50).
5. **Один эталон — BF16 off-веса.** Идея отдельного F16-GGUF эталона для
   llama.cpp отклонена. Таблицы две: controlled (vLLM-форматы FP8/NVFP4/AWQ/
   AutoRound на одной версии vLLM, bf16 KV) и GGUF на llama.cpp с пометкой
   «другой движок». Retention обеих таблиц считается от одного BF16.
6. **Старая ladder-кампания доделывается как есть** и публикуется как
   production-stack сравнение и поиск обрыва (2-1 бит), без клейма
   BF16-relative retention.
7. **Целевой коридор — 70–85% на семейство, не 40–80%** (уточнено 23.08 по
   данным калибровки). Причина: у нас парный дизайн, retention считается на
   задачах, которые проходит эталон. Задача, где BF16 плавает или падает, —
   выброшенный бюджет. Факт из калибровки: из 250 задач стабильно проходят
   193 (77%), флипают 31, не решаются 26. Худшие: word_ladder (годна 1 задача
   из 12) и rush_hour (3 из 12) — их облегчить или выкинуть, а не усложнять.
   Коридор 40–80% остаётся корректным для другого дизайна — ранжирования
   незнакомых моделей между собой (см. «Переиспользование сьюта»).
8. **Правило годности задачи (пред-регистрируется до прогона квантов).**
   Состав финального сета задаётся конфигами генераторов и стратами, а НЕ
   отбором отдельных задач: сначала генерим и замораживаем, потом гоним BF16.
   После этого действует заранее объявленное правило: основной retention
   считается на задачах, где эталон прошёл ВСЕ повторы; задачи, где эталон
   плавает или падает, из основного числа исключаются. Правило применяется
   к результатам эталона и фиксируется ДО первого прогона кванта, поэтому
   ни один квант не может на него повлиять. Рядом всегда публикуется
   pass rate по полному сету — чтобы отбор был виден и проверяем.
9. **Последовательность**: подготовка пула + префлайт-гейты → канарейка →
   калибровка xhigh через API (параллельными пачками, полдня) → freeze
   манифеста → BF16 на 4 efforts (~$25) → кванты на риге после лестницы
   (~2 суток) → анализ retention + поимённый список потерянных задач.

## Открытый вопрос: KV cache (поднят Алексеем 23.08.2026)

**Что выяснилось.** OpenRouter не раскрывает dtype KV-кэша ни для одного
провайдера. В метаданных эндпоинта 19 полей, квантизация ровно одна и она про
**веса**: пин `quantizations:["bf16"]` гарантирует bf16-веса у AkashML и ничего
не говорит про кэш. Из 8 эндпоинтов `qwen/qwen3.8-27b` bf16 по-прежнему только
AkashML, остальные fp8 (Alibaba — unknown).

**Чем гоняли мы.** Кампания 18.08 (та, что опубликована 20.08) шла на
квантованном кэше во всех движках: vLLM `--kv-cache-dtype fp8`, llama.cpp
`--cache-type-k q8_0 --cache-type-v q8_0`, NInfer `--kv-dtype int8`. Текущий
дневной драйвер (`serve-qwen38-autoround.sh`) уже переехал на
`--kv-cache-dtype bfloat16` и держит 262K на TP2 с KV-пулом 362K токенов.

**Почему это важно и в какую сторону врёт.** Смещение возможно с обоих концов
и знаки у них разные:

- если AkashML под bf16-весами держит fp8-кэш, эталон слабее настоящего BF16;
  задачи, где он из-за этого флипает, вылетают из парного набора по
  пред-регистрированному правилу, остаток смещён в сторону устойчивых задач, и
  retention квантов выходит **оптимистичнее** реальности;
- если у AkashML кэш чистый, а наши локальные армы стоят на fp8/q8, мы меряем
  веса и кэш вместе, а приписываем всё весам, и retention выходит
  **пессимистичнее** реальности.

**Что снимает вопрос.** Второй конец полностью в наших руках: решение 5 уже
требует bf16 KV в controlled-таблице, а в харнессе v2 локальной серверной части
ещё нет вообще, так что ретрофитить нечего. Первый конец закрывает канарейка,
если дать ей третий арм:

| Арм | Веса | KV | Смысл |
|---|---|---|---|
| A | bf16, AkashML | неизвестен | эталон как есть |
| B | bf16, риг TP4 | bf16 | чистая опорная точка |
| C | bf16, риг TP4 | fp8 | цена кванта кэша при неизменных весах |

B против A говорит, укладывается ли неизвестность AkashML в наш порог шума
(3–4 п.п.). C против B даёт цену квантованного кэша отдельно от весов и
одновременно ограничивает сверху то, чем AkashML мог бы нам подпортить эталон.

**Стоимость.** API-половина уже оплачена: `runs/ref-final/scored.jsonl` — 100
задач x 3 повтора на xhigh, канарейку набираем подмножеством. Платим только
ригом: ~20 задач это порядка 94K токенов на арм-повтор, ~25 мин при 60 tok/s,
итого около 2.5 GPU-часов на два арма по три повтора.

**Требование к подбору задач канарейки.** Ущерб от квантованного кэша растёт с
длиной контекста, поэтому подмножество стратифицируется по цене задачи в
токенах и обязано включать дорогие семейства (rush_hour ~51K, jugs ~27K). Набор
из одних дешёвых задач ответит только про короткие выводы.

**Архитектурная поправка.** Модель гибридная: реальный KV держат только 16
full-attention слоёв из 64, остальные 48 GDN идут через отдельный кэш состояния
(`--mamba-ssm-cache-dtype`). То есть `--kv-cache-dtype` трогает четверть слоёв,
bf16-кэш здесь дёшев, а эффект от fp8-кэша ожидаемо меньше, чем на обычной
dense-модели. Это гипотеза, её и меряет арм C.

**Что с опубликованным.** Ничего не отзывается. Кампания 18.08 сравнивала
кванты между собой на одном production-стеке, все армы на одинаковом
квантованном кэше, и решение 6 уже запретило ей клейм BF16-relative retention.
Отдельная оговорка на будущее: dtype кэша там различался между движками
(fp8 / q8_0 / int8), так что кросс-движковое сравнение внутри той кампании несёт
ещё и этот конфаунд.

### Обновление 24.08: distribution-пробник, арм A снят

Возражение Алексея: если pass rate у всех армов совпадёт, мы не опознаем
конфиг AkashML, и «fp8 не роняет качество» станет предположением. Возражение
справедливо по инструменту, а не по логике. При пороге шума 3-4 п.п. и
канарейке в 20 задач pass rate не различает почти ничего, так что совпадение
там означало бы отсутствие разрешения, а не равенство.

Поэтому канарейка получает второй, острый инструмент. Проверено живьём против
AkashML 24.08:

- `logprobs` и `top_logprobs` **работают**, но только с выключенным thinking
  (`reasoning:{enabled:false}`). С `reasoning_effort` единственный токен уходит
  в reasoning-канал и `logprobs` приходит пустым;
- **assistant prefill не поддерживается** — хвостовое assistant-сообщение
  выбрасывается (проверка: префикс «The capital of France is Par» дал
  продолжение «The capital of», то есть новый ход). Teacher-forced скоринг
  готовых трейсов отпадает.

Отсюда рабочая схема: длинный промпт → распределение **первого** сгенерированного
токена → top-20, температура 0. KV под тестом — это KV промпта, поэтому осью
служит длина промпта. Шума сэмплирования нет вообще.

Харнесс: `harness/kv_probe.py` (`build` / `run` / `compare`), промпты собираются
конкатенацией уже оплаченных трейсов из `runs/`, KL считается по
перенормированному top-20.

**Арм A снят**: `runs/kv-dist-akash.jsonl`, 20 промптов (5 на бакет 4K/16K/48K/
100K, фактические длины 3.5K-142K токенов), $0.40, провайдер проверялся на
каждом вызове.

Разрешающая способность подтверждена: распределения не вырождены, top-1 в
среднем 0.37-0.59, энтропия 1.5-2.0 нат, ни одного пробника с top-1 > 0.99.
Значит KL≈0 у рижных армов будет означать настоящее совпадение, а не слепоту
инструмента.

Осталось: армы B (bf16 KV) и C (fp8 KV) на риге, когда освободятся карты —
сейчас их держит `eval_carve.py` (стадия 3 карвинга).

Ограничение, которое надо назвать в публикации: пробник щупает off-путь, а
бенч гоняется в thinking-режимах. Dtype кэша — свойство attention-слоёв, а не
режима рассуждения, поэтому перенос разумен, но это допущение, а не измерение.

### Результат KV-канарейки, 24.08

Полный отчёт: [`llm-bench/results/quant-bench-v2-kv-canary-2026-08-24/`](../results/quant-bench-v2-kv-canary-2026-08-24/README.md).

| Сравнение | Что различается | median KL | top-1 |
|---|---|---:|---:|
| FLASH_ATTN vs FLASHINFER, оба bf16 KV | только бэкенд | 0.0089 | 20/20 |
| bf16 KV vs fp8 KV, один бэкенд | только dtype кэша | 0.0489 | 19/20 |
| AkashML vs риг bf16 KV | весь их стек | 0.0888 | 17/20 |
| AkashML vs риг fp8 KV | их стек + квант кэша | 0.1308 | 16/20 |

Токенизация совпала 20/20, распределения не вырождены — сравнение валидно.

Читается так: пол сантехники 0.0089, квант кэша даёт 0.0489 (в 5.5 раза выше
пола, но top-1 держится 19/20), а AkashML отстоит от нас на 0.0888 — дальше,
чем вся KV-ось. То есть решение держать локальные армы на bf16 KV подтверждено,
а вопрос доверия к API-эталону не закрыт, а переставлен: расхождение стека
больше того, из-за которого канарейку затевали.

Следующий шаг прежний — pass-rate канарейка на подмножестве уже оплаченного
`ref-final`: доезжает ли расхождение распределений до исходов задач. Платим
только ригом.

### Перепроверка 24.08: гейт эффорта снят, разрешение канарейки под вопросом

Полная перепроверка части 1 и части 2 — в конце
[отчёта канарейки](../results/quant-bench-v2-kv-canary-2026-08-24/README.md).
Коротко, что меняет протокол:

- **Регулятор эффорта на риге работает, старый гейт давал ложный FAIL.**
  vLLM 0.23 прокидывает верхнеуровневый `reasoning_effort` в шаблон; сама
  ручка — одна строка системного промпта, допустимы только `low`, `medium`,
  `xhigh`, причём **xhigh это дефолт**, а `medium` вообще не даёт системного
  сообщения; `high`/`max`/`none` шаблон отвергает с исключением. Живой тест без
  потолка: rg-propositional_logic-001 дал 400 -> 9 938 токенов (24.8x) против
  24.7x у эталона. Гейт переписан на low против xhigh с порогом 2x.
- **KL в отчёте на 58–62% состоит из штрафа `floor=1e-6` за токены вне top-20.**
  Порядок расхождений держится на любой метрике, но в публикацию нести JSD
  (бэкенд 0.0016 / dtype кэша 0.0065 / AkashML 0.0119), а не KL.
- **Квантовали четверть слоёв.** Модель гибридная, `--kv-cache-dtype fp8`
  трогает 16 слоёв из 64, SSM-кэш остался bf16 (флага
  `--mamba-ssm-cache-dtype` в скриптах нет). Оговорка обязательна везде, где
  называется цена кванта кэша.
- **У pass-rate канарейки не хватит разрешения.** Эталон проходит 3/3 только
  на 39 задачах из 47 (20 из них tool-calling, где он даёт 100%). McNemar
  exact становится значимым с 6 перевернувшихся задач, то есть канарейка
  различает лишь потерю **>=15 п.п.**; 5 п.п. дают p=0.50. Прогонять её как
  проверку на катастрофу можно, но «нет разницы» будет означать отсутствие
  разрешения. Прежде чем тратить 3-4 часа рига — решить: добавлять повторы на
  39 стабильных задачах или расширять пул нетривиальными задачами.
- **Потрачено по трейсам $49.54** (не ~$48.40).

## Переиспользование сьюта на других моделях

Харнесс и задачи модель-независимы: клиент бьёт в любой OpenAI-совместимый
`/v1`, верификаторы про модель ничего не знают. Переносится всё, кроме
калибровки — она привязана к тому, кого мы взяли эталоном.

- **Другая модель + её кванты** (тот же вопрос «что ломает квантование»):
  работает как есть. Нужно заново подобрать сложность под BF16 этой модели —
  для процедурных RG-семейств это правка конфига и перегон, для статики
  перевес страт. Целевой коридор тот же, 70–85%.
- **Сравнение моделей между собой** (лидерборд): задачи те же, но коридор
  другой — там уместны 40–80%, максимум различающей силы у задач, которые
  решает примерно половина. Плюс появляется проблема, которой нет в парном
  сравнении: **загрязнение**. AIME/HMMT/IFBench публичны, кто-то мог на них
  учиться. В сравнении квантов одной модели загрязнение сокращается (оно
  одинаково с обеих сторон), в сравнении разных моделей — нет.

Поэтому в манифесте финального сета фиксируется, под какой эталон он
калиброван, а конфиги генераторов хранятся по семействам, чтобы их можно было
перекрутить под другую модель, не трогая код.

## Goal

Measure quality loss caused by local weight quantization of the same model.
BF16 is the only reference. FP8, NVFP4, AWQ, GGUF and NInfer are candidates,
not references.

This is not a general model leaderboard. The primary signal is paired
retention against BF16 on the same frozen tasks, prompts, reasoning effort,
sampling contract and verifier.

## Non-negotiable protocol

- Final test tasks run at all four reasoning efforts: `off`, `low`, `medium`,
  `xhigh`.
- Do not impose a benchmark reasoning-token budget. Let the model stop
  naturally, subject only to the endpoint's real context/output ceiling.
- Preserve the complete response, reasoning trace, final answer, tool calls,
  finish reason, prompt/completion/reasoning token counts, latency and verifier
  trace for every attempt.
- Primary scores use programmatic or exact verifiers. LLM-as-judge may be
  reported only as a separate experimental metric.
- Freeze dataset revision, prompts, task IDs, generator parameters, seeds,
  verifier version, chat template and parser settings before any quant is run.
- Report endpoint/model tasks separately from agent/system tasks. Agent scores
  also depend on the harness, tool parser, context management and environment.
- Long-context scores are separate because they jointly measure weights, KV
  dtype and engine behavior.

## Calibration without cherry-picking

The target is a BF16 pass rate of 70--85% per family at `xhigh` (revised
2026-08-23; the earlier 40--80% band belongs to cross-model ranking, not to
paired retention). We do not choose individual test items because BF16
happened to pass or fail them once.

1. Build a broad development pool from the current sources below.
2. For procedural sources, tune family-level difficulty on development seeds.
3. Generate the final test set from disjoint, previously unused seeds.
4. For static sources, stratify by official difficulty/date/domain metadata,
   then sample and freeze IDs before examining quant results.
5. Run BF16 calibration repeats to estimate pass-rate uncertainty.
6. If a block misses 40--80%, change its difficulty stratum or generator
   parameters, not individual answers.
7. Freeze the suite. Only then run every quant.

## Current candidate pool

### Quant Core

| Source | Current pin | What it measures | Candidate target |
|---|---|---|---:|
| LiveBench | release `2026-06-25`; blocked until its questions are public | objective reasoning, coding, mathematics, data analysis, language and instruction following | 0 for now |
| Reasoning Gym | `49b07130b3fcd12f2d064bba7c43869543a0e7e7` | fresh procedural reasoning with exact verifiers and adjustable difficulty | 40--60 dev, 20--24 final |
| MathArena | 2026 competitions only | fresh contest mathematics with exact final answers | 12--20 dev, 8--10 final |
| IFBench | `db69a6f05689830b0068b8f1529ebcfd2f3b164c` | difficult OOD instruction constraints with programmatic verifiers | 16--24 dev, 8--12 final |
| BFCL v4 | current v4 revision to be pinned | native/prompt tool calling, arguments, parallel and multi-turn calls, relevance and format sensitivity | 16--24 dev, 8--12 final |
| LongBench Pro | 2026 release, HF revision to be pinned | realistic long-context understanding across fixed length bands | 16--24 dev, 8--12 final |

Reasoning Gym families to calibrate first:

- `cryptarithm` -- constraint solving;
- `graph_color` -- graph constraints;
- `jugs` -- multi-step planning;
- `word_ladder` -- search;
- `number_sequences` -- induction;
- `shortest_path` -- graph reasoning;
- `zebra_puzzles` -- multi-constraint logic;
- `propositional_logic` -- formal deduction;
- `rush_hour` or `sokoban` -- state-space planning;
- `intermediate_integration` -- symbolic mathematics.

The initial final-size target for Quant Core is 64--80 scenarios. It can only
be finalized after measured BF16 wall time and pass-rate calibration.

LiveBench's current leaderboard release is not the same thing as an available
evaluation dataset. The public runner currently exposes only older complete
question splits, so those downloaded files are inspection-only and cannot be
silently substituted for the 2026 release. A current rolling coding source
must replace this block if the 2026 questions remain unavailable.

### Agent Deep

| Source | Current pin | What it measures | Candidate target |
|---|---|---|---:|
| DeepSWE | v1.1, updated `2026-08-13` | original long-horizon repository engineering | 8--12 dev, 3--5 final |
| Terminal-Bench 3.0 | initial 2026 release | hard terminal work across seven domains | 8--12 dev, 2--4 final |
| MCPMark | current revision and MCP server images to be pinned | real filesystem, GitHub, PostgreSQL and browser tool workflows | 10--16 dev, 4--6 final |
| Toolathlon-Verified | final 2026 release | long-horizon multi-application tool use | 4--6 dev, 0--2 final |
| SWE-rebench V2 | frozen dated 2026 split | fresh real repository fixes | 6--10 dev, 2--4 final |

Agent Deep initially targets 12--16 scenarios. A source is excluded if BF16
cannot reach the 40--80% band under the fixed local agent harness.

## Explicitly retired from v2

The old campaign remains preserved and will be completed, but none of these
sources enter the new primary suite:

- HumanEval / HumanEval+;
- GSM8K and the current GSM-Symbolic pack;
- MMLU-Pro and GPQA Diamond;
- IFEval;
- AIME 2024/2025;
- current BenchLocal `lcb-v6-30` selection;
- publicly available old LiveBench question splits masquerading as the 2026
  leaderboard release;
- Aider Polyglot;
- old custom Hermes, CLI, bugfind, data-extraction and structured-output packs;
- LongBench v1/v2 and RULER;
- SWE-bench Verified and SWE-bench Pro.

HLE, ARC-AGI-3 and full Harbor-Index are not in the primary candidate pool:
they either introduce judge/scaffold variables or are likely to put this 27B
BF16 reference below the measurable floor. They can be revisited only if a
small development slice empirically reaches the calibration band.

## Primary reporting

For every block, model and effort:

- raw pass rate and confidence interval;
- paired retention: quant passes among tasks BF16 passes;
- BF16-to-quant regressions and quant-only wins by task ID;
- reasoning-token distribution and answer-token distribution;
- latency, output throughput and total wall time;
- finish-reason, truncation, parser and verifier-failure breakdown;
- tool-call validity and tool-step count for agent blocks;
- context length and KV dtype for long-context blocks.

The headline should never be one blended percentage. Publish Quant Core,
Agent Deep, Tool Calling and Long Context separately, followed by a clearly
labelled macro summary.

## Download snapshot, 2026-08-22

Server root: `/mnt/nvme2/datasets/local-quant-bench-v2`.

Downloaded repository revisions:

- Reasoning Gym `49b07130b3fcd12f2d064bba7c43869543a0e7e7`;
- IFBench `db69a6f05689830b0068b8f1529ebcfd2f3b164c`;
- MathArena `a11194deff8c67a232974a383795e8a2776b4c6f`;
- LiveBench runner `ac912b2e0aaa7adfb919d7454ae5aaaacc17342d`;
- BFCL `6ea57973c7a6097fd7c5915698c54c17c5b1b6c8`;
- DeepSWE `435ee89ec2f2e2289f33b0da4f992f0b7b7266b9`;
- Terminal-Bench 3 public `ff96555093c8bc7696bdc810aa5313e4a0690fee`;
- MCPMark `cd45b7f57923b9b3985467f5139927575f83141c`;
- Toolathlon `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`;
- SWE-rebench V2 tools `c71902a8cf8d2b725f63d51f199f4d3e56f68d2d`.

Downloaded Hugging Face snapshots include LongBench Pro at
`4996884deae51f5e5d23c88da9d857fc54e5fa15`, AIME 2026 at
`d2de22f3c656b4f56cf8981212186377d1e23bc3`, HMMT February 2026 at
`02fba4f74d8e68e73e66a02d540fd979c05c274c`, and the SWE-rebench V2 sample at
`9a7cd16b2431fc9f0abaf4c359e21fd3fae12ae3`.

The snapshot currently occupies about 1.7 GB. Git LFS payloads and benchmark
container images were intentionally not downloaded; they will be pulled only
for the final calibrated task subset.

## Предрегистрация анализа, 2026-08-24

Записано ДО того, как расширение набора отработало. Причина — сегодня утром
вывод по FP8 был получен на знаменателе, выбранном после факта, и оказался
артефактом. Чтобы это не повторилось, метод фиксируется заранее.

### Что пошло не так с первым расчётом

`harness/retention.py` считал долю удержания на задачах, которые эталон взял
3 из 3. Знаменатель, выбранный по результату эталона, делает выигрыш кванта
физически невозможным: на таких задачах он может только проиграть. Отсюда
«4 потери, 0 приобретений», которое я принял за направление эффекта. Без
отбора картина симметрична: 12 задач вниз, 9 вверх.

Тест тоже был не тот. McNemar считает потери и приобретения
взаимозаменяемыми, а правило отбора это запрещает. Корректный нулевой
эксперимент строится симуляцией, но он неустойчив: p-значение гуляет от 0.036
до 0.77 в зависимости от того, как сглаживать оценку вероятности задачи по
шести броскам. Опираться на него нельзя.

`retention.py` остаётся как описательная статистика и не несёт вывода.

### Оценка и вывод, зафиксированные заранее

Считает `harness/paired_diff.py`.

Оцениваемая величина, основная: среднее по задачам от (доля прохождения
кванта минус доля прохождения эталона), каждая доля по своим повторам на
xhigh. Одно число в пунктах точности на замороженном наборе. Ни по одному
арму ничего не отбирается.

Интервал — парный бутстрап по задачам. P-значение — перестановка знаков.

Обработка совпадений. Доли кратны 1/3, поэтому на первой сотне **13.9%
перестановок попадают ровно на наблюдаемое значение**. Засчитывать их или нет
двигает p между 0.21 и 0.36, а сравнение сырых float ловит произвольную их
часть. Принята консервативная договорённость: совпадения засчитываются
против эффекта, сравнение с допуском, оценка `(h+1)/(B+1)`. Доля совпадений
печатается в отчёте.

Дополнительно и явно вторично: та же разница по каждому блоку; та же разница
на задачах, которые хоть раз решил хоть один арм (задачи на полу дают ровно
ноль, так что это только пересчёт масштаба, p не меняется); счёт сдвинувшихся
задач как описание.

### Что признаётся заранее

Стандартная ошибка на 300 задачах ожидается около 1.2 пункта против 2.1 на
ста. Если FP8 не теряет ничего, интервал выйдет примерно [-2.4, +2.4] и
вывод будет «стабильно в пределах 2.4 пункта». Если теряет наблюдённые 2.3
пункта, интервал будет около [-4.7, +0.1] и значимости впритык не хватит;
вывод тогда «потеря не больше 5 пунктов». Утверждение «падает ровно на X»
заранее не обещается: чтобы уверенно разрешить эффект в 2 пункта, нужно около
450 задач, а пул математики исчерпан уже на 300.

### Разложение дисперсии, на чём основан выбор

Дисперсия парной разницы на первой сотне: 49% шум измерения от трёх повторов,
51% реальный разброс между задачами. Повторы бьют только по первой половине
(3 → 8 повторов снижают ошибку с 2.12 до 1.76), задачи — по обеим. Поэтому
расширяется набор, а не число повторов.

### Расширение набора

`harness/freeze_ext.py`, +200 задач, `final-pool/extpool.jsonl`,
sha256 в `EXT-MANIFEST.json`, всего 300.

Ловушка reasoning_gym, найдена при сборке: соседние сиды НЕ дают независимых
задач. Сид 20260824 воспроизвёл последовательность сида 20260823, сдвинутую
на один элемент, то есть «новый сид» молча переиздал бы замороженные задачи.
Поймано проверкой на дубликаты. Решение: тот же сид, тот же поток, берётся
хвост за пределами замороженной головы. Поток не зависит от запрошенного
размера, а его голова в точности воспроизводит старые 40, поэтому
непересечение доказано, а распределение то же.

Отклонения по составу, обе вынужденные и записанные в манифест: AIME 2026 —
ноль новых задач, эталон решает его на 100%, такие задачи не могут
зарегистрировать потерю и только разбавляют оценку; HMMT — 11 задач, весь
остаток пула. Доля математики падает с 16% до 9%, освободившийся бюджет ушёл
в IFBench и BFCL как ближайшие к рабочей полосе 0.6–0.9.

Эталон расширения гоняется только на xhigh ×3: кривая эффорта уже измерена на
первой сотне и в дополнительной мощности не нуждается.

### Поправка к предрегистрации, 24.08: обрыв провайдера это не ошибка модели

Внесено после того, как стали видны трейсы эталона, но **до того, как хоть
один квантованный арм досчитал**. Правило записано заранее относительно того
результата, на который оно влияет.

Платный API вернул `finish_reason: "error"` с пустым ответом на **8 из 900**
своих генераций на `xhigh`. Это не разнос модели, а обрыв на стороне
провайдера, и вот доказательство: те же задачи спокойно доходят до конца на
других повторах самого эталона (`ma-hmmt_feb_2026-19` оборвался на 43 763
токенах и досчитал 91 217 на третьем проходе), а на риге FP8 прошёл все восемь
штатно, включая `ma-hmmt_feb_2026-27` на 117 072 токенах против 33 831, где
сдался API.

Локальный движок так упасть не может в принципе. Значит, засчитывая обрыв как
неверный ответ, мы занижаем только эталон и дарим **каждому** кванту фору
около 0.6 пункта при искомом эффекте порядка 2.3. Треть эффекта, причём
всегда в одну сторону.

**Правило.** Ответ с `finish_reason == "error"` либо с ошибкой драйвера
исключается из доли прохождения задачи как отсутствующие данные. Задача, у
которой не осталось ни одного валидного повтора хотя бы в одном арме, выходит
из парного анализа. Правило симметрично и применяется к любому арму, включая
локальные.

Направление поправки важно: она **поднимает** эталон (78.89 → 79.50 на
трёхстах задачах) и, стало быть, делает каждый квант хуже на 0.61 пункта.
Это поправка против себя, а не в свою пользу. На данных без обрывов она
пустышка: первая сотня дала те же −2.33 пункта и p = 0.354 до сотой доли.

**`finish_reason == "length"` НЕ исключается.** Потолок 131 072 токена одинаков
для всех армов, поэтому исчерпать его и не выдать ответа — это отказ модели, а
не отказ инфраструктуры. Одна генерация FP8 так и сделала и засчитана провалом.
Заодно это первое подтверждение гипотезы, что деградировавшие веса думают
дольше: эталон нигде не подошёл к потолку ближе 99 721 токена.

**Плановая замена правила.** Восемь оборванных генераций эталона будут
перегнаны заново (около доллара), после чего у всех задач снова будет по три
честных повтора и костыль не понадобится. Перегоняются именно **отсутствующие**
ответы, а не проваленные: перезапуск по признаку «модель ответила неверно» был
бы отбором по результату, то есть ровно той ловушкой, которая уже испортила
первый расчёт удержания. Обрыв провайдера результатом не является.

**Порог контекста, следствие того же наблюдения.** Медиана размышления на
`xhigh` около 1 500 токенов, но p99 доходит до 60–93 тысяч, а максимум у
эталона 93 416. У ступеней GGUF контекст на слот выставлен 98 304, то есть
запас всего 5%. Для нижних ступеней (Q2, IQ1), которые предположительно
многословнее, его надо поднимать: обрезанная по длине генерация зачтётся
провалом и мы намеряем нехватку контекста вместо потери качества. Освободившаяся
память это позволяет: у IQ1_M веса 7 ГБ против 23 у Q6.

## Поправка к предрегистрации, 25.08: отступ в начале ответа это след движка

При разборе Q6 нашёлся артефакт харнесса, который бил по блоку `if`.

**Что нашли.** Доля ответов блока `if`, начинающихся с пробела или переноса:

```
ref-final        60/60    100%
ref-ext         146/146   100%
quant-fp8        60/60    100%
quant-awq       206/206   100%
quant-awq-cloud 206/206   100%
quant-autoround 206/206   100%
quant-q6kml       0/205     0%
```

vLLM и API оставляют перенос строки после `</think>`, llama.cpp его срезает.
В блоке `if` есть требования вида «в выводе не должно быть пробельных
символов» и «начни с такого-то символа», поэтому llama.cpp получал даровой
проход, а все остальные даровой провал.

**Величина.** Q6 против эталона на блоке `if` давал +9.42 пп при p = 0.0106,
а головное число +2.50 пп при p = 0.0520. Единственное за весь прогон
сравнение, дотянувшее до значимости, оказалось разницей движков.

**Правка.** В `score_run.py` содержимое ответа теперь нормализуется
`.strip()` перед проверками. Отступ в начале это след шаблона чата, а не
выбор модели. Правка применена ко ВСЕМ армам одинаково, все скоры пересчитаны.

**После правки** блок `if` у эталона поднялся с 74.88% до 81.16%, у Q6 разница
упала до +3.14 пп (p = 0.2153), головное число до +1.06 пп (p = 0.3490).
Выводы по FP8, AWQ и AutoRound не изменились: у них и у эталона артефакт был
одинаковый и в парном сравнении сокращался.

## Поправка к предрегистрации, 25.08: клиентский таймаут

У `quant-q6kml` 19 генераций (15 задач, стадии xhigh r2/r3) умерли на
`TimeoutError` в клиенте харнесса. Это не отказ модели, а наш собственный
потолок ожидания: llama.cpp в 3-4 раза медленнее vLLM, и таймаут ловил самые
длинные генерации. У армов на vLLM таких обрывов ноль.

По правилу от 24.08 это пропуск данных. Но обрывы бьют по одному арму
избирательно, поэтому добавлена проверка на устойчивость: флаг
`--errors-as-failures` в `paired_diff.py` считает обрыв провалом модели.

```
Q6, обрыв = пропуск  : +1.06 пп  [-1.06, +3.11]  p = 0.3490
Q6, обрыв = провал   : +0.44 пп  [-1.67, +2.56]  p = 0.7619
```

Вывод не зависит от выбора правила.
