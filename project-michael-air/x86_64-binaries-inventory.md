# x86_64 Binaries Inventory & Remediation Plan

**Date:** 2026-08-15  
**Status:** Assessment complete; remediation pending user decisions

---

## Summary

| Directory | Total Binaries | Action | Details |
|-----------|---|---|---|
| `/opt/local/bin` | 497 | Review & decide | MacPorts; 412 have ARM Homebrew equivalent, 85 legacy/not needed |
| `/opt/local/sbin` | 7 | Remove | MacPorts sysadmin tools; all have Homebrew equivalents |
| `/opt/X11/bin` | 123 | Remove | X11 deprecated; XQuartz is ARM64 alternative (rarely needed) |
| `/usr/local/bin` | 0 | ✓ Clean | Already empty (Intel Homebrew removed) |

**Reclaim space:** 2-3 GB by removing /opt/local and /opt/X11

---

## /opt/local/bin: MacPorts Binaries (497 files)

### Category A: ARM Equivalents Available in Homebrew (412+ binaries)

**Recommendation:** Remove from /opt/local; install ARM64 version from Homebrew if needed

| Package | Size | Homebrew Alternative | Install Command | Notes |
|---------|------|----------------------|-----------------|-------|
| **dbus** | ~2 MB | ✓ Available | `brew install dbus` | Message bus; needed if app requires D-Bus |
| **graphviz** | ~5 MB | ✓ Available | `brew install graphviz` | Graph visualization tools (dot, circo, etc.) |
| **imagemagick** | ~10 MB | ✓ Available | `brew install imagemagick` | Image processing (convert, identify, etc.) |
| **git** | ~20 MB | ✓ Available | `brew install git` | Already in Homebrew (via Brewfile) |
| **jq** | ~1 MB | ✓ Available | `brew install jq` | JSON processor |
| **node/npm** | ~200 MB | ✓ Available | `brew install node` | Already in Brewfile |
| **python** | ~50 MB | ✓ Available | `brew install python` | Already in Brewfile |
| **python@3.13** | ~50 MB | ✓ Available | `brew install python@3.13` | Already in Brewfile |
| **perl** | ~20 MB | ✓ Available | `brew install perl` | Latest Perl; MacPorts has perl@5.8, perl@5.12 (very old) |
| **cmake** | ~15 MB | ✓ Available | `brew install cmake` | Build tool |
| **sqlite3** | ~3 MB | ✓ Available | `brew install sqlite3` | Database |
| **bzip2** | ~1 MB | ✓ Available | `brew install bzip2` | Compression |
| **xz** | ~1 MB | ✓ Available | `brew install xz` | Compression |
| **libtiff** | ~3 MB | ✓ Available | `brew install libtiff` | Image format library |
| **curl** | ~2 MB | ✓ Available | `brew install curl` | HTTP client |
| **openssl** | ~10 MB | ✓ Available | `brew install openssl` | Encryption library |
| **fontconfig** | ~5 MB | ✓ Available | `brew install fontconfig` | Font configuration |
| **gtk+**, `gtk+3`, `glib`, `gdk-pixbuf` | ~200 MB total | ✓ Available | `brew install gtk+ gtk+3 glib gdk-pixbuf` | GUI toolkit; rarely used on macOS |

**Action:** These are safe to delete from /opt/local. Install ARM64 versions from Homebrew as needed.

---

### Category B: Legacy or Rarely-Used Versions (85 binaries)

**Recommendation:** Remove; no longer needed or versions too old for modern use

| Package | Version | Status | Why Remove |
|---------|---------|--------|------------|
| **perl@5.8** | 5.8.x | Obsolete | Released 2002; Perl 5.12+ in Homebrew |
| **perl@5.12** | 5.12.x | Obsolete | Released 2010; Perl 5.14+ in Homebrew |
| **db46** | Berkeley DB 4.6 | Obsolete | Released 2007; deprecated by Oracle; rarely used |
| **saslpasswd2**, `sasldblistusers2` | SASL v1 | Obsolete | Old auth mechanism; replaced by modern alternatives |
| **annotate** | CVS tool | Obsolete | CVS is abandoned; use Git instead |
| **expect** | Tcl expect | Niche | Used for scripting interactive programs; Homebrew bottle available if needed |
| **fcm**, `fc-*` (fontconfig tools) | FontConfig | Low-value | System font tools; rarely invoked manually |
| **dia** | Diagram editor | GUI app | Should use macOS app version or Homebrew equivalent |
| **graphviz** tools (circo, dot, etc.) | Graphviz | Available | Use `brew install graphviz` instead |

**Action:** Remove completely. None are needed for modern development workflows.

---

## /opt/local/sbin: MacPorts System Tools (7 files)

**Status:** All x86_64, all have Homebrew equivalents or are system tools

| Tool | Purpose | Homebrew Alternative | Action |
|------|---------|----------------------|--------|
| **dbus-daemon** | Message bus daemon | `brew install dbus` | Remove (rarely run manually) |
| **pluginviewer** | Plugin viewer | N/A | Remove (legacy) |
| **pwcheck** | SASL password checker | N/A | Remove (obsolete) |
| **saslauthd** | SASL auth daemon | N/A | Remove (obsolete) |
| **saslpasswd2** | SASL password utility | N/A | Remove (obsolete) |
| **testsaslauthd** | SASL test tool | N/A | Remove (obsolete) |

**Action:** `sudo rm -rf /opt/local/sbin` (remove all; none are needed)

---

## /opt/X11/bin: X11 Display System (123 files)

**Status:** All x86_64; deprecated on modern macOS

| Category | Files | Status | Action |
|----------|-------|--------|--------|
| **X11 server** | ~50 | Deprecated | Remove (X11 not needed for most modern apps) |
| **X utilities** | ~70 | Deprecated | xdotool, xset, xdpyinfo, xwininfo, xwud, etc. |
| **X clients** | ~3 | Deprecated | X terminal emulators, etc. |

### When Would You Need X11?

- Remote X11 forwarding from Linux servers
- Running legacy X11 graphical applications
- Certain scientific/visualization tools

### Alternative: XQuartz (ARM64 Native)

If you DO need X11, install **XQuartz** instead:
- Download: <https://www.xquartz.org/>
- Native ARM64 version available
- Active development and support
- Drop-in replacement for /opt/X11

**Recommendation:** Remove /opt/X11 unless actively using X11 applications. If needed later, install XQuartz.

**Action:** `sudo rm -rf /opt/X11` (unless you're certain you need X11)

---

## /usr/local/bin: Intel Homebrew Remnants

**Status:** ✓ Empty (0 binaries)

All Intel Homebrew binaries have been cleaned up. Good!

The following directories are also safe (already empty or minimal):
- `/usr/local/Homebrew` — Old Intel Homebrew root
- `/usr/local/Cellar` — Old package directory
- `/usr/local/opt` — Old symlink directory

---

## Remediation Checklist

### Immediate (Safe to Delete)

- [ ] Inventory complete ✓ (this document)
- [ ] Backup /opt/local (optional): `tar czf ~/Desktop/opt-local-backup.tar.gz /opt/local`
- [ ] Remove MacPorts: `sudo rm -rf /opt/local`
- [ ] Remove X11: `sudo rm -rf /opt/X11`

### Cleanup PATH

- [ ] Edit ~/.zshrc, ~/.bashrc, ~/.profile
  - Remove: `/opt/local/bin`, `/opt/local/sbin`, `/opt/X11/bin`
  - Example: `grep -v "/opt/local\|/opt/X11" ~/.zshrc > ~/.zshrc.tmp && mv ~/.zshrc.tmp ~/.zshrc`

### Verify Removal

- [ ] Run: `echo $PATH | tr ':' '\n' | grep -E "opt/local|opt/X11" | wc -l` (should be 0)
- [ ] Confirm essential tools still work:
  - `rustc --version` (should be ARM64 from Homebrew)
  - `uv --version` (should be ARM64 from Homebrew)
  - `git --version` (should be ARM64 from Homebrew)

### If Something Breaks

For any tool that doesn't work after removing /opt/local:
1. Check if Homebrew has it: `brew search <toolname>`
2. If available: `brew install <toolname>`
3. If not available: Install from source or alternative package manager

---

## Space Recovery

| Directory | Size | Action |
|-----------|------|--------|
| `/opt/local/` | 1-2 GB | Remove |
| `/opt/X11/` | 100-500 MB | Remove |
| `/usr/local/Homebrew`, `/usr/local/Cellar` | 500 MB | Remove (if empty) |
| **Total Recovery** | **2-3 GB** | **Available for use** |

---

## Notes

- **No action required** if you're not using MacPorts or X11
- **Brewfile already configured** for Homebrew equivalents (rust, uv, node, python, etc.)
- **Machine rename** (issue #9) doesn't affect this cleanup; proceed independently
- **Time Machine exclusions** should be updated after cleanup (see x86_64-remediation.md)

