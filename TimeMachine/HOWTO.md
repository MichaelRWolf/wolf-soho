# How to use the GrandPerspective analysis scripts

## 1. Create an export in GrandPerspective

1. Open GrandPerspective and scan the volume or folder you care about (e.g. your home directory).
2. Use **File → Export to Text File** (or equivalent).
3. Save as a tab-separated value file (`.tsv`): first line `Path` and `Size`, then one path and size (bytes) per line.
4. Note the path to the export file.

## 2. Run the scripts

Pass the export file path (`.tsv`) to each script:

```bash
cd TimeMachine
./by_directory /path/to/export.tsv
./by_application /path/to/export.tsv
./by_filetype /path/to/export.tsv
```

Each script prints lines of the form: **size_in_bytes** **label** (e.g. directory name, app name, or extension), sorted by size descending.

## 3. Interpret the output

- **by_directory** — Find which top-level folders (e.g. Pictures, Library, Music) use the most space. Good for deciding what to move to NAS or prune.
- **by_application** — Find which apps (under Application Support, Caches, Containers) use the most space. Good for clearing caches or uninstalling heavy apps.
- **by_filetype** — Find which extensions (e.g. .mov, .pack, .ipa) dominate. Good for targeting video, git repos, or installers.

Re-run after cleanups or a new scan to see updated totals.
