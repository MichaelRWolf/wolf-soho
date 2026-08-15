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

## Setup Priority Levels

**High:** Shell, Homebrew, PATH setup — blocks CLI development  
**Medium:** Privacy/TCC fixes, account investigation, data accounting  
**Low:** Time Machine efficiency audit and exclusion decisions

See [setup.md](setup.md) for detailed checklist with rationale.

## Key Issues Being Tracked

**Intel x86_64 Binaries:** Apple silently migrated incompatible binaries. See [GitHub issue #8](https://github.com/MichaelRWolf/wolf-soho/issues/8) for audit strategies.

**23.42 GB "Other Files & Folders":** Unknown contents from Migration Assistant. Needs audit (search strategies in [setup.md](setup.md)).

**~/Library (27.59 GB):** Mixed valuable + regenerable content. Must measure by size + file count before making exclusion decisions.

## Markdown Conventions

Follow [~/.claude/CLAUDE.md](https://github.com/anthropics/claude-code) global conventions:
- No hard newlines in prose (emacs soft-wrap)
- Use `##` / `###` headings and lists for structure
- Markdown only (no `.org` files)
