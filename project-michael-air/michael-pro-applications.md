# michael-pro Applications Inventory

**Source:** Extracted from Time Machine restore to michael-air (2026-08-13/14)  
**Note:** Modification dates reflect restore time, not original install dates. Actual install dates from michael-pro backup are not recoverable via CLI.

**Status:** Use this list to compare against michael-air current state and decide what to keep/reinstall.

---

## Applications Recovered

| Application | Size | Restored Date | Likely Source | Notes |
|-------------|------|---------------|----------------|-------|
| 1Password | 535 MB | 2026-08-12 | App Store | Password manager; synced via 1Password account |
| 1Password for Safari | 132 MB | 2026-08-17 | Safari Extension | Companion extension |
| BackupLoupe | 20 MB | 2026-05-19 | Other | Time Machine backup browser utility |
| Claude (Claude Code) | 801 MB | 2026-08-15 | Direct Download | Anthropic's Claude Code IDE |
| CotEditor | 126 MB | 2026-08-06 | App Store | Text editor with syntax highlighting |
| Daylite | 122 MB | 2026-08-13 | Direct Download | marketcircle.com — Calendar/Contacts via CalDAV/CardDAV |
| Docker | 2.1 GB | 2026-08-06 | Direct Download | Container platform |
| Emacs | 505 MB | 2026-07-25 | Homebrew | Emacs text editor (likely homebrew-installed) |
| GIMP | 803 MB | 2026-04-17 | Other | Image editor (likely Homebrew or MacPorts) |
| GitHub Desktop | 681 MB | 2026-08-11 | Direct Download | GitHub client |
| Google Chrome | 707 MB | 2026-08-11 | Direct Download | Web browser |
| GrandPerspective | 7.0 MB | 2026-05-31 | App Store | Disk usage visualization |
| Install macOS Tahoe | 17 GB | 2026-08-14 | System | macOS upgrade installer (can delete) |
| MarkText | 311 MB | 2026-06-04 | Other | Markdown editor (likely Homebrew) |
| MenuMeters | 4.6 MB | 2021-11-12 | Other | System menu bar CPU/memory/network monitor |
| Pieces OS | 2.8 GB | 2026-08-06 | Direct Download | Code snippet manager |
| Pieces | 297 MB | 2026-07-29 | Direct Download | Pieces companion app |
| Quicksilver | 18 MB | 2026-04-19 | Direct Download | Launcher (verified working on michael-air) |
| Rectangle | 9.4 MB | 2026-07-15 | App Store | Window tiling manager |
| Safari | 0 B | 2025-02-04 | System | System browser |
| Typora | 46 MB | 2026-08-05 | Direct Download | Markdown editor (note: paid) |
| kdiff3 | 341 MB | 2026-03-01 | Homebrew | 3-way file diff tool |
| noTunes | 1.2 MB | 2024-07-08 | Other | Disable Apple Music in iTunes (lightweight) |

---

## Summary Stats

| Metric | Value |
|--------|-------|
| Total Applications | 24 |
| Total Size | ~16 GB |
| Homebrew Likely | Emacs, MarkText, kdiff3, GIMP(?) |
| App Store | 1Password, CotEditor, GrandPerspective, Rectangle |
| Direct Download | Claude, Daylite, Docker, GitHub Desktop, Chrome, Pieces, Quicksilver, Typora, noTunes |
| System | Safari, Install macOS Tahoe (delete when done) |

---

## Next Steps: michael-air Comparison

1. **Review this list** and note what you actually use
2. **Get current michael-air state:**
   ```bash
   ls -1 /Applications/*.app | xargs -I {} basename {} .app
   ```
3. **Identify gap:**
   - What's missing from michael-air that you want?
   - What's on michael-air that you don't need?
4. **Reinstall via Homebrew/App Store:**
   - Update Brewfile for tools (Emacs, kdiff3, MarkText, etc.)
   - Install from App Store for subscriptions
   - Direct download for specialized tools (Docker, Daylite, Typora, etc.)

---

## Notes on Source Attribution

- **Homebrew:** Apps typically installed via `brew install --cask`; reinstall with Brewfile
- **App Store:** Synced via Apple ID; re-download from App Store app
- **Direct Download:** Look for official installers or homebrew-cask equivalents
- **System:** Built into macOS; not reinstalled
- **Dates:** Modification dates reflect Time Machine restore (2026-08-13/14), not original install dates from michael-pro
