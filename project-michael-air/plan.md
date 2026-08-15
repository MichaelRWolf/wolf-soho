# michael-air Setup Plan

## TODO

### Time Machine Configuration

- [ ] Retrieve TM exclusion rules from NAS backup of michael-pro
  - **NAS location:** Check `/Volumes/[nas-name]/[backup-name].sparsebundle` for Time Machine backup data
  - **Settings file:** `~/Library/Preferences/com.apple.TimeMachine.plist` (user level)
  - **System settings:** `/Library/Preferences/com.apple.TimeMachine.plist` (system level)
  - **Note on ~/Library:** Time Machine automatically includes `~/Library` by default. This creates a bind-22: it backs up configuration (gold), but also backs up cache/state that may not be portable across OS versions and can confound configuration restoration. Monitor for config creep from old machine state.
  - **michael-pro status:** Dead (water damage, no SSH access). Only option is manual extraction from NAS backup or manual reconstruction from current machine rules.

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
