# analyze_GrandPerspective

Scripts to summarize a GrandPerspective text export (Path, Size per line) by directory, application, or file type. Use the summaries to find large consumers and plan disk cleanup.

**Input:** A tab-separated value (`.tsv`) export from GrandPerspective: first line `Path\tSize`, then one path and byte size per line.

**Contents:**

- `by_directory` — total size per top-level directory under the scan root.
- `by_application` — total size per app under Library (Application Support, Caches, Containers).
- `by_filetype` — total size per file extension.
- `verify-tm-isexcluded` — TAP script to verify Time Machine include/exclude paths (uses `tm-exclude-include.yaml`).
- [HOWTO.md](HOWTO.md) — how to create an export and run the scripts.
- [HOWTO_exclude_items_from_TM.md](HOWTO_exclude_items_from_TM.md) — TM exclusions and verification.

Put GrandPerspective export files (`.tsv`) in this directory or elsewhere and pass the path to each script.
