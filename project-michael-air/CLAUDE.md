# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**project-michael-air** tracks purchase, setup, and configuration of a new MacBook Air (M3, 13-inch, 2024) to replace michael-pro (water damaged). Primarily project documentation, not a software project.

**Hardware:**
- Model: MacBook Air (M3, 2024)
- RAM: 16 GB | Storage: 256 GB SSD
- OS: macOS 15.7 Sequoia
- Status: Time Machine restore completed 2026-08-13/14; setup in progress

**Related:**
- [GitHub issue #6](https://github.com/MichaelRWolf/wolf-soho/issues/6) — michael-pro water damage incident
- [GitHub issue #8](https://github.com/MichaelRWolf/wolf-soho/issues/8) — Intel x86_64 binary audit (stays open)
- `project-macbook-x2-reshuffle` — Broader MacBook reshuffling
- `wolf-soho` (global) — Main SOHO infrastructure repo

## File Guide

| File | Purpose | Update Frequency |
|------|---------|------------------|
| [README.md](README.md) | Project overview, quick status, hardware specs | On major status change |
| [setup.md](setup.md) | Migration process, issues found, setup checklist (high/medium/low priority) | As setup progresses |
| [tm-strategy.md](tm-strategy.md) | Time Machine efficiency audit framework and measured data | As data gathered |
| [x86_64-remediation.md](x86_64-remediation.md) | Intel binary audit results, replacement strategy, remediation plan | Post-audit, stays open |
| [x86_64-binaries-inventory.md](x86_64-binaries-inventory.md) | Categorized inventory of x86_64 binaries and Homebrew equivalents | Reference |
| [PATH-verification-proposal.md](PATH-verification-proposal.md) | Strategic proposal: validate PATH entries by command execution, not just file existence | Decision pending |
| [x86_64-audit.sh](x86_64-audit.sh) | Automated audit script: scans system for Intel-only binaries and incompatibilities | Reusable |
| [X11-and-XQuartz.md](X11-and-XQuartz.md) | X11 migration path for future wolf-air retirement | Archive/reference |
| `images/` | Screenshots from Migration Assistant restore (for reference) | Never (archive) |

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

## Setup Priority Levels

**High:** Shell, Homebrew, PATH setup — blocks CLI development  
**Medium:** Privacy/TCC fixes, account investigation, data accounting  
**Low:** Time Machine efficiency audit and exclusion decisions

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
```

**Related repositories:**
- **[portable-profile](https://github.com/MichaelRWolf/portable-profile)** — Manages shell startup files (.profile, .bashrc, .zshrc) and includes PATH setup logic. Changes here affect michael-air's shell environment.
- **[wolf-soho](../)** — Main infrastructure repo. Contains macOS/network device registry (CONTEXT.md) and global CLAUDE.md guidance.

## Key Issues Being Tracked

**Intel x86_64 Binaries:** Apple silently migrated incompatible binaries. See [GitHub issue #8](https://github.com/MichaelRWolf/wolf-soho/issues/8) for audit strategies and [x86_64-remediation.md](x86_64-remediation.md) for removal plan.

**PATH Pollution:** Broken binaries (Intel on ARM) add clutter to PATH. See [PATH-verification-proposal.md](PATH-verification-proposal.md) for proposed execution-test strategy (pending decision).

**23.42 GB "Other Files & Folders":** Unknown contents from Migration Assistant. Needs audit (search strategies in [setup.md](setup.md)).

**~/Library (27.59 GB):** Mixed valuable + regenerable content. Must measure by size + file count before making exclusion decisions.

## Markdown Conventions

Follow [~/.claude/CLAUDE.md](https://github.com/anthropics/claude-code) global conventions:
- No hard newlines in prose (emacs soft-wrap)
- Use `##` / `###` headings and lists for structure
- Markdown only (no `.org` files)
