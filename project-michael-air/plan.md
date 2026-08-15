# michael-air Setup Plan

## Migration & Restore (Completed 2026-08-13/14)

- [x] Time Machine restore from NAS via Setup Assistant (2026-08-13/14)
  - Restored ~106 GB from Synology NAS backup of michael-pro
  - Selected accounts: Michael R. Wolf (75.95 GB), mmac-shared (10.4 MB), Annie Nomous (20.6 MB)
  - Applications (17.6 GB), System & Network settings, Other Files & Folders (23.42 GB unaccounted)
  - See [migration-log.md](migration-log.md) for full details

## High Priority: Shell & Development Environment

- [ ] Update macOS to latest version (from 15.7 Sequoia)
- [ ] Fix login shell (currently Intel `/usr/local/bin/bash`, causes Terminal failure)
  - Immediate: `chsh -s /bin/zsh`
  - Permanent: Link to `/opt/homebrew/bin/bash` after ARM Homebrew installed
- [ ] Inventory Intel Homebrew (before deletion)
  - `find /usr/local/Cellar -maxdepth 1 -mindepth 1 -type d -exec basename {} \; | sort`
- [ ] Install native ARM Homebrew under `/opt/homebrew`
- [ ] Update PATH and shell startup files for ARM Homebrew
- [ ] Remove Intel Homebrew tree after validation
  
## Medium Priority: Privacy & Permissions

- [ ] Fix ~/Downloads TCC/privacy issue (Migration Assistant damaged access)
  - System Settings → Privacy & Security → Files & Folders → Terminal → Downloads
- [ ] Audit full TCC permissions restored from migration
  - Check Full Disk Access, Spotlight indexing, Calendar/Contacts access

## Medium Priority: Account Investigation

- [ ] Investigate mmac-shared account (10.4 MB, unknown origin)
- [ ] Investigate Annie Nomous account (20.6 MB, unknown origin)
- [ ] Delete or repurpose these accounts based on findings

## Time Machine Efficiency Audit

See [tm-audit.md](tm-audit.md) for full framework.

- [ ] Account for "Other Files & Folders" (23.42 GB) from migration
- [ ] Measure ~/Library by size and file count
- [ ] Classify caches, logs, IDE state, package caches by recovery value
- [ ] Identify high-file-count, low-value directories (major restore bottleneck)
- [ ] Decide Time Machine exclusions based on measured data + regeneration cost
- [ ] Document all decisions for next machine migration

## Launcher & Shortcuts Recovery

- [ ] Verify Command-Space binding (Spotlight vs. third-party launcher)
- [ ] Restore launcher preferences from migrated state

## Log

### Saturday, 2026-08-15

#### Completed

- [x] Clone github.com repos to ~/repos (2026-08-15)
  - 31 repos cloned; excluded ~/repos from Time Machine backups

| Repository                | Last Pushed | Days |  Size (KB) |
|---------------------------|-------------|-----:|----------:|
| Acura_Integra_LS_1995     | 2025-12-12  | 246  |         0 |
| FY-2025                   | 2026-07-02  |  43  |        36 |
| MichaelRWolf.github.io    | 2026-04-10  | 126  |         8 |
| SOHO                      | 2025-03-31  | 501  |         1 |
| Second_Brain              | 2026-04-07  | 130  |       353 |
| adventure                 | 2026-07-02  |  44  |         0 |
| bloom-technical-marketing | 2026-07-30  |  15  |        11 |
| chatgpt-tools             | 2026-07-02  |  43  |         0 |
| chatgpt-utilities         | 2026-07-02  |  44  |         0 |
| claude-tools              | 2026-07-22  |  24  |         0 |
| daylite-replacement       | 2026-07-02  |  44  |         0 |
| dotfiles                  | 2026-07-22  |  24  |         0 |
| events                    | 2026-08-03  |  11  |        13 |
| git-tools                 | 2026-07-13  |  33  |         0 |
| gs-vehicle-maintenance    | 2024-09-12  | 701  |         0 |
| harmony-united            | 2026-07-02  |  43  |         0 |
| health-michael            | 2025-11-04  | 283  |         0 |
| job-search                | 2026-07-22  |  24  |        93 |
| notes                     | 2026-07-07  |  38  |         0 |
| personal-finances         | 2026-04-24  | 112  |         0 |
| portable-profile          | 2026-08-14  |   0  |        11 |
| recipes                   | 2025-11-07  | 281  |         0 |
| rv-2003-dutchman          | 2026-07-22  |  24  |        30 |
| shortcuts                 | 2026-07-02  |  43  |         0 |
| trails-end                | 2025-10-04  | 314  |         0 |
| trails-end-campground     | 2026-07-30  |  16  |       148 |
| wendy-ai                  | 2026-07-20  |  25  |         0 |
| white-box                 | 2026-07-20  |  25  |        39 |
| wisdom                    | 2026-07-22  |  24  |         1 |
| wolf-soho                 | 2026-08-14  |   0  |        16 |
| writing                   | 2026-07-13  |  33  |        15 |

### Friday, 2026-08-14

(backfill)

### Thursday, 2026-08-13

(backfill)
