# Licensing proposal before release

The repository currently has no top-level license. Do not imply that embedded
third-party benchmark prompts are relicensed by this dataset.

Recommended split for the public release:

- **MIT** for original scripts and harness code authored for these campaigns.
- **CC BY 4.0** for original measurements, aggregate tables, documentation,
  and charts, to the extent the repository owner holds those rights.
- **Upstream terms unchanged** for benchmark prompts/tests embedded inside raw
  requests and result files. `ATTRIBUTION.md` enumerates them, including
  GSM-Symbolic's CC BY-NC-ND 4.0 terms and LiveCodeBench's source notice.
- **No model-weight redistribution**; only links, pinned revisions, launch
  metadata, and generated outputs are included.

Once the owner confirms this split, add the complete MIT and CC BY 4.0 texts at
the repository root and point this file to them. Until then, this file is a
release checklist, not a license grant.
