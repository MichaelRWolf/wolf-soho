# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**project-michael-air** tracks purchase, setup, and configuration of a new MacBook Air (M3, 13-inch, 2024) to replace michael-pro (water damaged). Primarily project documentation, not a software project.

**Hardware:**
- Model: MacBook Air (M3, 2024)
- RAM: 16 GB | Storage: 256 GB SSD
- OS: macOS 15.7 Sequoia
- Status: Migration complete (2026-08-13/14); x86_64 remediation done (2026-08-16); Time Machine exclusions finalized (2026-08-17)

**Related:**
- [GitHub issue #6](https://github.com/MichaelRWolf/wolf-soho/issues/6) — michael-pro water damage incident
- [GitHub issue #8](https://github.com/MichaelRWolf/wolf-soho/issues/8) — Intel x86_64 binary audit (stays open)
- `project-macbook-x2-reshuffle` — Broader MacBook reshuffling
- `wolf-soho` (global) — Main SOHO infrastructure repo

## File Guide

| File | Purpose | Status |
|------|---------|--------|
| [README.md](README.md) | Project overview, quick status, hardware specs | Current |
| [setup.md](setup.md) | Migration process, issues found, setup checklist | Mostly complete; monitor for regressions |
| [PLAN-names-networks-backups.md](PLAN-names-networks-backups.md) | Time Machine, machine naming, NAS config — comprehensive execution plan | Complete (Phase 1-6) |
| [tm-strategy.md](tm-strategy.md) | TM efficiency audit framework, exclusion rationale, xattr management | Final (2026-08-17) |
| [2026-08-17_tm-exclusions-analysis.md](2026-08-17_tm-exclusions-analysis.md) | TM exclusion audit results and correctness assessment | Final |
| [x86_64-remediation.md](x86_64-remediation.md) | Intel binary audit results, removal plan, PATH cleanup | Complete (2026-08-16) |
| [x86_64-binaries-inventory.md](x86_64-binaries-inventory.md) | Categorized x86_64 binary inventory and Homebrew equivalents | Reference |
| [x86_64-audit.sh](x86_64-audit.sh) | Automated audit: scans for Intel-only binaries and incompatibilities | Reusable |
| [tmutil_analysis](tmutil_analysis) | Script: checks TM exclusions (tmutil + xattr markers) | Use for verification |
| [PATH-verification-proposal.md](PATH-verification-proposal.md) | Strategic proposal for execution-test PATH validation | Deferred (low ROI) |
| [X11-and-XQuartz.md](X11-and-XQuartz.md) | X11 migration path for future wolf-air retirement | Archive/reference |
| `images/` | Migration Assistant restore screenshots | Archive |

## Workflow

### Checking Status
- See [README.md](README.md) for quick overview and completion percentage
- See [setup.md](setup.md) **Part 3: Setup Checklist** for detailed TODO status (✓ done, ⏳ pending)

### Updating Progress
1. Complete a setup task from [setup.md](setup.md) checklist
2. Mark the item `[x]` and add date (e.g., `(2026-08-15)`)
3. If new finding: add under "Part 2: Intel → ARM Issues" with status label (✓ FIXED, ⏳ TODO, etc.)
4. Commit with clear message describing what was done

### Time Machine Audit
- Use [tm-strategy.md](tm-strategy.md) framework to measure and decide exclusions
- Record all measurements and decisions **before deleting anything**
- Update decision table in [tm-strategy.md](tm-strategy.md) as audit progresses

### Documenting Issues
1. If blocking issue: create/link GitHub issue (e.g., [issue #8](https://github.com/MichaelRWolf/wolf-soho/issues/8))
2. If investigation finding: add to [setup.md](setup.md) under appropriate section
3. Keep findings in project files, not external notes

## Investigation & Remediation Workflow

This project follows a **measure → decide → validate → implement** pattern:

1. **Audit phase** (e.g., `x86_64-audit.sh`) — Scan system non-destructively, produce log
2. **Analysis** — Parse results, categorize findings (e.g., [x86_64-binaries-inventory.md](x86_64-binaries-inventory.md))
3. **Strategy** — Propose solution with trade-offs (e.g., [PATH-verification-proposal.md](PATH-verification-proposal.md))
4. **Remediation plan** — Document action steps and validation (e.g., [x86_64-remediation.md](x86_64-remediation.md))
5. **Update checklist** — Mark completed items in [setup.md](setup.md) Part 3 with date

**Key principle:** Never delete or remove anything without first measuring, documenting, and deciding. All decisions are recorded in project files (not external notes) so they remain discoverable.

## Time Machine Operations

**Exclude a path (via CLI when GUI won't work, e.g., dotfiles):**
```bash
# Via tmutil (system-wide, persistent)
tmutil addexclusion <path>
tmutil addexclusion -p <path>         # Persistent (survives TM reset)

# Via xattr (Apple's native marker, takes precedence)
xattr -w com.apple.metadata:com_apple_backup_excludeItem "bplist00_com.apple.backupd" <path>

# Remove exclusion
tmutil removeexclusion <path>
xattr -d com.apple.metadata:com_apple_backup_excludeItem <path>
```

**Audit & validate:**
```bash
./tmutil_analysis                      # Complete exclusion report (tmutil + xattr)
tmutil isexcluded <path>               # Single path check
defaults read /Library/Preferences/com.apple.TimeMachine  # View config
```

**Key principle:** User excludes regenerable paths (repos, caches, apps, downloads). Apple auto-excludes system cruft via xattr. See [tm-strategy.md](tm-strategy.md) for rationale & [PLAN-names-networks-backups.md](PLAN-names-networks-backups.md) Phase 5 for configuration.

## Setup Priority Levels

**High:** Shell, Homebrew, PATH setup — blocks CLI development  
**Medium:** Privacy/TCC fixes, account investigation, data accounting  
**Low:** Time Machine efficiency audit and exclusion decisions (mostly complete)

See [setup.md](setup.md) for detailed checklist with rationale.

## Common Investigation Commands

**Run architecture/binary audit:**
```bash
./x86_64-audit.sh  # Generates x86_64-audit.log with comprehensive system scan
```

**Check file architecture (single binary):**
```bash
file /opt/local/bin/port              # See: Mach-O 64-bit executable x86_64 (or arm64)
lipo -info /usr/local/bin/some_binary # See: architectures in binary
```

**Account for disk space:**
```bash
du -xhd 1 / 2>/dev/null | sort -h     # System-wide breakdown
du -xhd 3 ~/ 2>/dev/null | sort -h    # Home directory breakdown
```

**Check Time Machine exclusions/size:**
```bash
system_profiler SPStorageDataType      # See TM backup size & exclusions

# View TM configuration plist
defaults read /Library/Preferences/com.apple.TimeMachine

# Check TM exclusions via tmutil
tmutil destinationinfo                 # Show current backup destination
tmutil isexcluded <path>               # Check if path is excluded

# Use project script (shows both tmutil + xattr markers)
./tmutil_analysis                      # Comprehensive TM exclusion audit
```

**Related repositories:**
- **[portable-profile](https://github.com/MichaelRWolf/portable-profile)** — Manages shell startup files (.profile, .bashrc, .zshrc) and includes PATH setup logic. Changes here affect michael-air's shell environment.
- **[wolf-soho](../)** — Main infrastructure repo. Contains macOS/network device registry (CONTEXT.md) and global CLAUDE.md guidance.

## Key Issues & Status

**✓ RESOLVED — Intel x86_64 Binaries (Issue #8)**
- Audit completed (2026-08-15): 289 KB log, 9-part analysis
- Remediation done (2026-08-16): Rust/uv rebuilt, /opt/local + /opt/X11 removed, PATH cleaned
- See [x86_64-remediation.md](x86_64-remediation.md) for details

**✓ RESOLVED — Time Machine Contamination**
- Backup excluded 5 high-impact paths: /Applications, ~/Downloads, ~/Pictures, ~/.cache, ~/repos
- Apple auto-excludes 70+ system/ephemeral directories via xattr
- Exclusions finalized 2026-08-17; see [2026-08-17_tm-exclusions-analysis.md](2026-08-17_tm-exclusions-analysis.md)
- Remaining task: Delete contaminated local/NAS snapshots and rebuild clean (Phase 6 of PLAN)

**⏳ PENDING — Snapshot/Share Cleanup**
- Local snapshots: 3 contaminated backups (470GB total system cruft) need deletion
- NAS share: `Backups-TM-Michael-Air` needs verification/rebuild
- See [PLAN-names-networks-backups.md](PLAN-names-networks-backups.md) Phase 6 for remediation steps

**⏳ DEFERRED — PATH Verification Strategy**
- [PATH-verification-proposal.md](PATH-verification-proposal.md) proposes execution-test validation
- Decision (2026-08-16): Defer due to low ROI (problem already solved by cleanup)

## Markdown Conventions

Follow [~/.claude/CLAUDE.md](https://github.com/anthropics/claude-code) global conventions:
- No hard newlines in prose (emacs soft-wrap)
- Use `##` / `###` headings and lists for structure
- Markdown only (no `.org` files)
