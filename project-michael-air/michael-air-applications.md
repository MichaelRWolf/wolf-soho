# michael-air Applications Inventory

**Snapshot Date:** 2026-09-28 (today)  
**Source Machine:** michael-air (M3 MacBook Air, 13", 256GB)  
**Prior Inventory:** [michael-pro-applications.md](michael-pro-applications.md) (recovered 2026-08-13/14)

**Generated:** `find /Applications -maxdepth 1 -name "*.app" -type d` with `du -sh` and `stat`

---

## System / Standard macOS Apps

| Application | Size   | Version | Modified   | Notes                                |
|-------------|--------|---------|------------|--------------------------------------|
| Safari      | System | 26.6.2  | (built-in) | Built-in web browser; always present |

---

## Personally Installed Applications

### Productivity & Development

| Application      |   Size | Version | Last Modified | Source/Notes                           |
|------------------|-------:|---------|---------------|----------------------------------------|
| 1Password        | 535 MB | 8.12.33 | 2026-08-12    | Password manager; synced via 1Password |
| 1Password Safari | 391 MB | 8.12.37 | 2026-09-16    | Companion browser extension (updated)  |
| CotEditor        | 126 MB | 7.0.8   | 2026-08-06    | Text editor with syntax highlighting   |
| Emacs            | 492 MB | 31.1    | 2026-09-21    | Text editor; via Homebrew (updated)    |
| GitHub Desktop   | 681 MB | 3.6.4   | 2026-08-11    | GitHub client                          |
| MarkText         | 311 MB | 0.19.1  | 2026-06-04    | Markdown editor                        |
| Quicksilver      |  18 MB | 2.6.0   | 2026-04-19    | Application launcher                   |
| Rectangle        | 9.4 MB | 0.98    | 2026-07-15    | Window tiling manager                  |
| Typora           |  46 MB | 1.14.10 | 2026-09-23    | Markdown editor (paid license)         |

### Web & Communication

| Application   | Size   | Version            | Last Modified | Source/Notes                     |
|---------------|----- --|------------------|----|----------------------------------|
| ChatGPT       | 1.3 GB | 26.825.31414      | 2026-08-27    | OpenAI ChatGPT desktop app (new) |
| Discord       | 479 MB | 0.0.411           | 2026-09-16    | Chat/voice platform (new)        |
| Google Chrome | 1.4 GB | 151.0.7922.173    | 2026-08-11    | Web browser                      |
| zoom.us       | 469 MB | 7.1.9 (88375)     | 2026-09-24    | Video conferencing (new)         |

### Utilities & Tools

| Application      |   Size | Version   | Last Modified | Source/Notes                                                    |
|------------------|-------:|-----------|---------------|-----------------------------------------------------------------|
| BackupLoupe      |  20 MB | 3.15.1    | 2026-05-19    | Time Machine backup browser                                     |
| Daylite          | 249 MB | 2026.37.0 | 2026-09-16    | Calendar/Contacts; Direct build from marketcircle.com (updated) |
| GrandPerspective | 7.0 MB | 3.7.2     | 2026-05-31    | Disk usage visualization                                        |
| MenuMeters       | 4.6 MB | 2.1.6.1   | 2021-11-12    | System menu bar: CPU/memory/network monitor                     |
| NetSpot          |  17 MB | 5.1.4967  | 2026-08-24    | WiFi signal mapping tool (new; diagnostic)                      |
| noTunes          | 1.2 MB | 3.5       | 2024-07-08    | Disable Apple Music in iTunes                                   |

### Code & Snippets

(None currently installed)

### Media & Reading

| Application   | Size   | Version | Last Modified | Source/Notes        |
|---------------|--------|---------|---------------|---------------------|
| Amazon Kindle | 280 MB | 7.67    | 2026-09-16    | E-book reader (new) |

---

## Removed / Cleaned (2026-09-28)

| Application | Size   | Version | Removed    | Reason                                                       |
|-------------|--------|---------|------------|--------------------------------------------------------------|
| Pieces OS   | 2.9 GB | 12.6.2  | 2026-09-28 | Bloat; disabled in Brewfile 2026-09-18; unneeded (issue #13) |
| Pieces      | 297 MB | 6.1.0   | 2026-09-28 | Bloat; disabled in Brewfile 2026-09-18; unneeded (issue #13) |

---

## Summary

| Metric               |  Count | Total Size  |
|----------------------|-------:|-------------|
| System apps          |      1 | (built-in)  |
| Personally installed |     19 | ~7.1 GB     |
| **TOTAL**            | **20** | **~7.1 GB** |

---

## Comparison: michael-air vs. michael-pro

### On michael-pro but NOT michael-air

- **Claude (Claude Code)** -- 801 MB -- Now installed as CLI (`brew install claude-code`), not in /Applications
- **Docker** -- 2.1 GB -- Not installed (bloat-heavy for light workflow)
- **GIMP** -- 803 MB -- Not reinstalled; use `imagemagick` CLI or lightweight alternatives
- **kdiff3** -- 341 MB -- Not installed; use built-in git diff or Homebrew as needed

### NEW on michael-air (vs. michael-pro)

- **Amazon Kindle** -- 280 MB -- E-book reading
- **ChatGPT** -- 1.3 GB -- OpenAI desktop app
- **Discord** -- 479 MB -- Chat platform
- **NetSpot** -- 17 MB -- WiFi diagnostic tool
- **zoom.us** -- 469 MB -- Video conferencing

### Size changes (updated versions)

- **Daylite** -- 249 MB (was 122 MB) -- Direct build from marketcircle.com; larger binary
- **1Password for Safari** -- 391 MB (was 132 MB) -- Companion extension growth
- **Emacs** -- 492 MB (was 505 MB) -- Minor variation

---

## Using This List for Reinstall/Updates

### If reinstalling on this machine or another

1. **Quick reference:** Use the "Personally Installed" tables above to identify what to reinstall
2. **Group by source:**
   - **App Store apps:** Sync via Apple ID in App Store app
   - **Homebrew:** `brew list --cask` to see installed; `brew install <app>` to reinstall
   - **Direct downloads:** Check official download pages (no auto-update)
   - **CLI tools:** Check portable-profile repo and Makefile
3. **Large apps to reconsider:**
   - ChatGPT (1.3 GB) -- Overlap with Claude Code CLI
   - Discord (479 MB) -- Web version often sufficient

---

## Prior Inventory

For historical context and comparison: **[michael-pro-applications.md](michael-pro-applications.md)** (recovered from Time Machine, 2026-08-13/14)
