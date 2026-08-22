# wendy-air Project: MacBook Air (M3) Setup & Migration

**Status:** In progress; awaiting machine purchase and delivery.

## Overview

Replacement for `wendy-pro` (water damaged, 2026-08). New machine: MacBook Air (M3, 13-inch, 2024).

Simplified setup using lessons from [project-michael-air](../project-michael-air/). Reuses audit scripts and Time Machine strategy.

## Quick Status

### ⏳ Pending

- Machine purchase and delivery
- Time Machine restore
- Shell & Homebrew setup
- Intel x86_64 audit and remediation
- Time Machine configuration

## Hardware Specs

(To be updated after purchase)

- **Model:** MacBook Air (13-inch, M3, 2024)
- **Processor:** Apple M3
- **RAM:** TBD
- **Storage:** TBD SSD
- **OS:** macOS Sequoia (or later)

## File Guide

| File                                       | Purpose                                                | Status    |
|--------------------------------------------|--------------------------------------------------------|-----------|
| [setup.md](setup.md)                       | Migration issues, setup checklist, TODO                | Current   |
| [machine_purchase.md](machine_purchase.md) | Specs comparison (M1/M2/M3) & michael-air reference    | Reference |
| [x86_64-audit.sh](x86_64-audit.sh)         | Automated Intel binary audit (reused from michael-air) | Ready     |
| [tmutil_analysis](tmutil_analysis)         | Time Machine exclusion audit (reused from michael-air) | Ready     |
| [CLAUDE.md](CLAUDE.md)                     | Claude Code guidance                                   | Current   |

## Related

- [project-michael-air](../project-michael-air/) -- Source of template & lessons learned
- [machine_purchase.md](machine_purchase.md) -- Specs & purchasing guidance
- [CONTEXT.md](../CONTEXT.md) -- Device registry
