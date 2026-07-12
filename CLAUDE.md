# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**wolf-soho** is a Small Office/Home Office (SOHO) infrastructure repository that documents and manages a distributed network spanning two locations (RV and Moe's house) plus personal computing devices. It combines documentation, monitoring scripts, and tooling for network operations.

**Key characteristic**: This is NOT a traditional software product -- it is primarily documentation (Markdown + shell scripts for operational automation). There are no application tests, builds, or releases. Quality is enforced through linting and tool functionality verification.

## Repository Structure

### Documentation (Location-based)

- **CONTEXT.md** - Canonical registry: device names, IPs, SSIDs, accessories. **Read this first for any network-related session.**
- **network_*.md** - Network topology and variant configurations (RV, home, PtP link)
- **equipment_*.md** - Detailed specs for computing, networking, portable devices
- **Ubiquiti/** - Point-to-point (PtP) RF link setup, config, operations
- **GL-iNet/** - beryl router SSH/UCI cheat sheet
- **ATT/** - Email/password troubleshooting (Yahoo + ATT)
- **Trails_End/**, **Atlassian/**, **Synology/**, etc. - Device/vendor-specific docs
- **PROJECT_*.md**, **2026-*.md** - Incident/project logs and recovery procedures

### Tools

- **bin/** - Utility scripts (shell, Python)
  - `network_location` - Determine RV/home network location
  - `nighthawk-signal`, `beryl_sqm` - Live monitoring stats
  - `fleet-status`, `fleet-nas-sync` - Multi-repo git workflow
  - `gitnas-*` - NAS-based remote git operations
  - `uplink-*` - Ubiquiti PtP monitoring
- **launchd/** - macOS scheduled agents (e.g., daily NAS sync)

## Development Workflow

### Setup

```bash
make help                  # Show all available targets
make install               # Install all project tools (symlinks + uplink commands)
make setup-hooks           # Configure pre-commit hooks
```

### Linting & Verification

Pre-commit hooks run automatically on `git commit` -- they enforce:

- **Markdown**: markdownlint (with fixed alignment via markdown-table-formatter)
- **Shell scripts**: shellcheck
- **Python**: ruff (linting + auto-formatting)
- **Text**: ligature/smartquote/dash normalization

**Important**: Do NOT use `--no-verify`. If hooks fail, fix the underlying issue and re-commit.

To lint manually before committing:

```bash
pre-commit run --all-files          # Run all hooks
pre-commit run -k shellcheck        # Run only shellcheck
pre-commit run -k markdownlint-fix  # Run only markdown linting
```

### Testing

```bash
make verify_TM_exclusions  # Test Time Machine exclusion list (Perl prove framework)
```

### Uninstall

```bash
make uninstall             # Remove all installed tools
uninstall_launchd          # Unload macOS scheduled agents
```

## High-Level Architecture

### Device Registry & Naming

All documentation uses canonical names from CONTEXT.md. This prevents ambiguity when discussing:

- Network devices: `beryl` (GL.iNet router), `loco-ap` / `loco-station` (Ubiquiti PtP), `spectrum-router` (Moe's home)
- Computing: `michael-pro`, `wolf-air`, `wendy-pro`
- SSIDs: `running-wolf-router`, `running-wolf-ptp`, etc.

**When writing or updating docs, use these names exactly -- do not invent alternatives.**

### Network Topology

Two independent locations connected by a point-to-point (PtP) RF link:

- **RV side**: beryl (main router) ↔ loco-station (RF transmitter) with POE injector
- **Moe's side**: spectrum-router (ISP) ↔ loco-ap (RF receiver) with POE injector
- **Bridge**: PtP operates on `running-wolf-ptp` SSID, 5.0 GHz, typically 867 Mbps link speed

Detailed setup in Ubiquiti/HOWTO_rascally_raccoon_PtP_*.md.

### Multi-Repo Git Workflow

Project provides tools for managing a fleet of git repos across multiple machines and a NAS:

- **gitnas-repo-setup**: Create bare repo on NAS + add remote in local repo
- **fleet-status**: Summarize uncommitted changes, unpushed commits across ~/repos/*
- **fleet-nas-sync**: Batch push all repos to NAS remote (with connectivity guard)
- **fleet-nas-sync** launchd agent: Runs daily at 16:00; logs to ~/Library/Logs/fleet-nas-sync.log

## Key Files by Use Case

| Goal                          | File                                           | Key Info                           |
|-------------------------------|------------------------------------------------|------------------------------------|
| Understand device names/IPs   | CONTEXT.md                                     | Canonical registry                 |
| Set up PtP link               | Ubiquiti/HOWTO_rascally_raccoon_PtP_install.md | Physical + RF alignment            |
| Troubleshoot PtP performance  | Ubiquiti/HOWTO_ubiquiti_loco_ptp_operations.md | Health checks, signal tuning       |
| Debug email login             | ATT/password_fuckery.md                        | Browser/OTP issues, workarounds    |
| Manage RV network remotely    | GL-iNet/beryl-cheat-sheet.md                   | SSH, UCI CLI commands              |
| Install project tools         | Makefile                                       | `make install` target              |
| Add/remove git repos to fleet | bin/fleet-status, bin/gitnas-*                 | Workflow examples in Makefile help |

## Common Tasks

### Add a new monitoring script

1. Create script in `bin/` with shebang (`#!/usr/bin/env bash` or `#!/usr/bin/env python3`)
2. Add to `BIN_FILES` in Makefile
3. Run `make install` to create symlink in ~/bin/
4. shellcheck will lint on commit

### Update SSID or device name

1. Edit CONTEXT.md with new canonical name + specs
2. Search project for old name: `git grep "old-name"`
3. Update all references in docs and scripts
4. All usages must match CONTEXT.md exactly

### Document a network incident or recovery

1. Create file: `YYYY-MM-DD_incident-name.md` (e.g., `2026-06-18_michael-pro_water-damage.md`)
2. Include: problem statement, steps taken, root cause, resolution, timeline
3. Link from relevant subsystem doc (e.g., equipment_computing.md)
4. Commit with clear message

## Markdown Conventions

- **Line length**: No hard limit (files use soft-wrap; emacs M-q unfills, not fills)
- **Table alignment**: markdown-table-formatter auto-aligns on commit
- **No .org files**: Pre-commit hook forbids org-mode files (3 already committed; do not add more)
- **Ligature/smartquote/dash**: Auto-normalized on commit (texthooks)

## Critical Constraint: Keweenaw County (Copper Harbor) -- Zero Cellular Coverage

**Keweenaw County has NO cellular coverage. NO LTE, NO 4G, NO emergency cell service. This is permanent.**

All internet at Trails End must be WiFi-based (Trails End Crew mesh, Beryl bridge, or PtP links). **Do NOT plan infrastructure around cellular hotspots or cell modems.** Devices like Netgear Nighthawk M1 are useless in Copper Harbor.

Infrastructure decisions must assume: WiFi-only, no cellular fallback, no mobile internet ever.

## Common Gotchas

1. **Pre-commit hook: markdown-table-formatter requires npm locally**. If `npx markdown-table-formatter` fails, install Node.js and re-run.
2. **Ubiquiti PtP link setup is picky about RF alignment.** See Ubiquiti/HOWTO_* docs before attempting physical install.
3. **Device names in CONTEXT.md are the source of truth.** Don't create aliases or shorthand -- use canonical names everywhere.
4. **beryl router is GL.iNet, not Ubiquiti.** It runs OpenWrt and uses UCI, not Ubiquiti's web UI. See GL-iNet/beryl-cheat-sheet.md.
5. **Time Machine exclusion tests require Perl prove framework.** `make verify_TM_exclusions` checks symlink resolution for TimeMachine/ entries.
6. **Keweenaw County has ZERO cell coverage.** Never assume cellular internet; it will never be available in Copper Harbor. All infrastructure must be WiFi-based.

## When to Ask About

- **Network troubleshooting**: Always read CONTEXT.md first to confirm device names; check Ubiquiti/HOWTO_ubiquiti_loco_ptp_operations.md for link health
- **Email config**: See ATT/password_fuckery.md before debugging Safari vs Chrome behavior
- **Adding new tools**: Makefile shows symlink pattern; add to BIN_FILES, commit, run `make install`
- **Device recovery**: Look for `2026-*.md` incident logs; may have step-by-step procedures documented
