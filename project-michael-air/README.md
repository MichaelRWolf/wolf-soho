# michael-air Project: MacBook Air (M3) Setup & Migration

**Status:** High-priority tasks complete (2026-08-13 to 2026-08-17); ongoing validation.

## Overview

Replacement for `michael-pro` (water damaged, recovered via Time Machine). New machine is a MacBook Air (M3, 13-inch, 2024).

**Purpose:** This project serves as both a case study and reusable template for setting up ARM MacBook Air machines via Time Machine restore. See [TEMPLATE-macbook-air-setup.md](TEMPLATE-macbook-air-setup.md) for reusable flow; see [project-wendy-air](../project-wendy-air) for application to the second water-damaged machine.

## Quick Status

### ✓ Completed (2026-08-13 to 2026-08-16)

- Time Machine restore from NAS (106 GB)
- Shell fixed (Intel bash → system zsh → Homebrew bash)
- Intel Homebrew removed (/usr/local/Homebrew, /opt/local, /opt/X11: 1.6 GB reclaimed)
- Rust & UV rebuilt (ARM64 native)
- X86_64 audit completed; findings documented
- Time Machine destination configured (NAS share: Backups-TM-Michael-Air)
- Exclusions set (GUI: ~/Downloads, ~/Pictures, ~/repos, ~/.cache; CLI: /opt/homebrew)

### ⏳ Ongoing (Validation & Monitoring)

- Time Machine backups running hourly -- monitor for errors
- Verify clean snapshots (user data only, no system files)
- Legacy backup share decision (keep or archive `Backups-TM-Michael`)

### 🔗 GitHub Issues

- [#6](https://github.com/MichaelRWolf/wolf-soho/issues/6) -- michael-pro water damage incident (closed)
- [#8](https://github.com/MichaelRWolf/wolf-soho/issues/8) -- x86_64 binary audit (reference)

## File Guide

### Setup & Migration (Use These for Future Machines)

| File                                                               | Purpose                                                                   |
|--------------------------------------------------------------------|---------------------------------------------------------------------------|
| **[TEMPLATE-macbook-air-setup.md](TEMPLATE-macbook-air-setup.md)** | **← START HERE** -- Reusable setup flow for wendy-air and future machines |
| [setup.md](setup.md)                                               | Migration issues encountered and fixes applied (michael-air specific)     |
| [x86_64-remediation.md](x86_64-remediation.md)                     | Intel binary audit, removal strategy, tool reference                      |
| [x86_64-binaries-inventory.md](x86_64-binaries-inventory.md)       | Detailed inventory of x86_64 artifacts (reference)                        |

### Time Machine (Configuration & Troubleshooting)

| File                                                             | Purpose                                                     |
|------------------------------------------------------------------|-------------------------------------------------------------|
| **[tm-reference.md](tm-reference.md)**                           | Quick reference: TM commands, exclusions, troubleshooting   |
| [tm-strategy.md](tm-strategy.md)                                 | Decision framework: what to backup, how to measure impact   |
| [PLAN-names-networks-backups.md](PLAN-names-networks-backups.md) | Full setup: NAS account creation, Keychain, hostname change |

### Project Metadata

| File                   | Purpose                                     |
|------------------------|---------------------------------------------|
| [CLAUDE.md](CLAUDE.md) | Claude Code guidance for this project       |
| `images/`              | Screenshots from Migration Assistant        |
| `tmutil_analysis`      | Script: audit TM configuration & exclusions |

## Hardware Specs

- **Model:** MacBook Air (13-inch, M3, 2024)
- **MPN:** A3113
- **Processor:** Apple M3 (8-Core GPU)
- **RAM:** 16 GB | **Storage:** 256 GB SSD
- **OS:** macOS 15.7 Sequoia
- **Seller:** gadgetpickup (eBay, 99.9% feedback)

## Quick Links

- **Setting up next machine?** → Start with [TEMPLATE-macbook-air-setup.md](TEMPLATE-macbook-air-setup.md)
- **TM troubleshooting?** → See [tm-reference.md](tm-reference.md)
- **Intel binary issues?** → See [x86_64-remediation.md](x86_64-remediation.md)
- **Full NAS + TM setup?** → See [PLAN-names-networks-backups.md](PLAN-names-networks-backups.md)
- **Related:** [wolf-soho](../) main repo | [project-wendy-air](../project-wendy-air) (wendy-pro replacement)
