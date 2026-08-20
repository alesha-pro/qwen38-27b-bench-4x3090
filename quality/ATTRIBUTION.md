# Attribution and data terms

No model weights are included. The repository stores measurements, model
outputs, launch metadata, and the benchmark inputs embedded in raw requests.

## Models

- [Qwen/Qwen3.8-27B-FP8](https://huggingface.co/Qwen/Qwen3.8-27B-FP8), Apache-2.0.
- [unsloth/Qwen3.8-27B-NVFP4](https://huggingface.co/unsloth/Qwen3.8-27B-NVFP4), Apache-2.0. The campaign's local HF metadata pinned an earlier revision that is recorded in `METHODOLOGY.md`.
- [cyankiwi/Qwen3.8-27B-AWQ-INT4](https://huggingface.co/cyankiwi/Qwen3.8-27B-AWQ-INT4), Apache-2.0.
- [unsloth/Qwen3.8-27B-GGUF](https://huggingface.co/unsloth/Qwen3.8-27B-GGUF), Apache-2.0.
- [neroued/Qwen3.8-27B-NInfer](https://huggingface.co/neroued/Qwen3.8-27B-NInfer), Apache-2.0.

## Harness and standard packs

[noonghunna/benchlocal-cli](https://github.com/noonghunna/benchlocal-cli) is
MIT-licensed and ports the MIT-licensed BenchLocal packs from `stevibe/*`.
The exact base commit, local patch, upstream attributions, and scenario source
commits are retained under `raw/harness/` and in the raw result metadata.

## Reasoning packs

- HumanEval+ derives from
  [evalplus/humanevalplus](https://huggingface.co/datasets/evalplus/humanevalplus), Apache-2.0.
- LiveCodeBench derives from
  [livecodebench/code_generation_lite](https://huggingface.co/datasets/livecodebench/code_generation_lite). The project repository is MIT-licensed; its HF dataset card declares the broad `cc` label and the underlying problems originate from competition platforms. Preserve source attribution when redistributing these raw inputs.
- GSM-Symbolic derives from
  [apple/GSM-Symbolic](https://huggingface.co/datasets/apple/GSM-Symbolic), CC BY-NC-ND 4.0. Its prompts are reproduced as received inside benchmark requests; no ownership or relicensing of those prompts is claimed here.
- GPQA-Diamond data is not included because the gated pack was never materialized.

The public measurements and analysis are a compilation around these sources.
Nothing in this repository overrides third-party licenses for embedded prompts,
tests, or model artifacts.
