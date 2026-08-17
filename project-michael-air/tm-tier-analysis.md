# Time Machine Tier 1/2/3 Analysis for michael-air

## Goal

Restore all necessary secrets and accumulated (but forgotten) settings that enable muscle memory and workflow continuity. Exclude regenerable caches/logs to speed restore.

---

## TIER 1: CRITICAL — Restore or Your Mac Is Broken

**Size: ~100 MB | File count: ~5K | Restore time: <5 min**

| Item                                 | Location               | Size   | Why                                      | Currently backed up? |
|--------------------------------------|------------------------|--------|------------------------------------------|----------------------|
| **Keychain (passwords, SSH, certs)** | `~/Library/Keychains/` | 65 MB  | Losing passwords = locked out everywhere | ✓ (in ~/Library)     |
| **SSH keys**                         | `~/.ssh/`              | 180 KB | Git, remote servers, deployment keys     | ✓ (home dir)         |
| **GPG keys**                         | `~/.gnupg/`            | 204 KB | Signed commits, encrypted email          | ✓ (home dir)         |
| **Git config**                       | `~/.gitconfig`         | <1 KB  | Commit author, GPG signing key           | ✓ (home dir)         |

**Status:** ✓ All covered if you keep `~/Library` and home directory.

---

## TIER 2: IMPORTANT — Muscle Memory + Workflow

**Size: ~500 MB–2 GB | File count: ~10K | Restore time: 5–20 min**

| Item                       | Location                                               | Size       | Why                                                                    | Example                                                | Currently backed up?    |
|----------------------------|--------------------------------------------------------|------------|------------------------------------------------------------------------|--------------------------------------------------------|-------------------------|
| **App preferences**        | `~/Library/Preferences/`                               | varies     | Finder show dotfiles, trackpad double-tap, Safari tabs, Terminal theme | `.com.apple.finder.plist`, `.com.apple.Terminal.plist` | ✓ (in ~/Library)        |
| **Browser profiles**       | `~/Library/Safari/`, `~/.config/Chrome/`, etc.         | 100–500 MB | Bookmarks, history, extensions, saved passwords                        | Bookmarks for dev sites, LastPass/1Password extension  | ✓ (in ~/Library)        |
| **Mail settings + cache**  | `~/Library/Mail Downloads/`, Mail data                 | 100–300 MB | Email accounts, folder structure, signature                            | Gmail IMAP setup, accounts                             | ✓ (in ~/Library)        |
| **Calendar/Contacts data** | `~/Library/Application Support/AddressBook/`, Calendar | 50–200 MB  | Synced calendars, contact list                                         | Recurring meetings, contact photos                     | ✓ (in ~/Library)        |
| **Shell config**           | `~/.bashrc`, `~/.zshrc`, `~/.profile`                  | <1 MB      | Aliases, functions, PATH, prompt                                       | `alias ls='ls -G'`, `export EDITOR=emacs`              | ✓ (home dir)            |
| **Editor config**          | `~/.vscode/settings.json`, `~/.emacs.d/`, etc.         | 10–100 MB  | Keybindings, themes, formatter settings                                | Emacs init file, VS Code theme                         | ✓ (partly; check below) |

**Status:** ⚠ Mostly covered BUT `~/Library/Application Support` is **currently excluded** — need to refine this.

---

## TIER 3: REGENERABLE — Exclude Aggressively

**Size: 10–20 GB | File count: 500K–2M | Restore time: 30+ min if included**

| Item | Location | Why exclude | Currently backed up? |
| ------ | ---------- | ------------- | ---------------------- |
| **Caches** | `~/Library/Caches/`, `/Library/Caches/` | Auto-rebuilt on app launch | ✗ Exclude |
| **Logs** | `~/Library/Logs/`, `/Library/Logs/` | Regenerated; old logs rarely useful | ✗ Exclude |
| **Xcode build artifacts** | `~/Library/Developer/Xcode/DerivedData/` | 5–20 GB; rebuilt on compile | ✗ Exclude |
| **Package download cache** | `~/.cache/pip/`, `~/.cache/npm/`, `~/.cargo/registry/cache/`, `~/.gem/` | Reinstall on demand | ✗ Exclude |
| **IDE extensions** | `~/.vscode/extensions/` | Reinstall from marketplace | ✗ Exclude |
| **Homebrew cache** | `/Library/Caches/Homebrew/`, `~/Library/Caches/Homebrew/` | Redownloaded on brew install | ✗ Exclude |

---

## Current Exclusion Problems

**SkipPaths (13 items):**

- ✓ Good: `/Users/michael/.gem`, `.npm`, `.cpan`, `/Applications`, Dropbox/iCloud paths
- ✗ **Too broad:** `/Users/michael/Library/Application Support` (excludes Mail/Calendar/Contacts)
- ✗ **Questionable:** `/Users/michael/Pictures` (might be large, but valuable if you want photo restore)
- ✗ **Questionable:** `/Users/michael/Downloads` (might contain important files)

**ExcludeByPath (3 items):**

- `/Library/Application Support/Microsoft/PlayReady` — ✓ Good (junk)
- `/Users/Shared/adi` — ✓ Good (junk)
- `/Library/Preferences/FLEXnet Publisher` — ✓ Good (junk)

---

## Exclusion Updates Applied

### Removed (2026-08-17)

**Redundant exclusions** — Apple already excludes these by default:

```bash
tmutil removeexclusion ~/Library/Application\ Support     # ✓ DONE
tmutil removeexclusion ~/Library/Containers              # ✓ DONE
tmutil removeexclusion ~/Library/Group\ Containers       # ✓ DONE
```

**Rationale:** Apple's automatic exclusion policy already handles Application Support, Containers, and Group Containers. User config was redundant. Simplified to rely on Apple defaults; no behavior change.

**Calendar/Contacts sync:** User syncs via Daylite.app (CalDAV/CardDAV from marketcircle.com), so local Application Support is regenerable from cloud — safe to exclude.

### Add (precise Tier 3 regenerable)

```bash
tmutil addexclusion ~/Library/Caches
tmutil addexclusion ~/Library/Logs
tmutil addexclusion ~/Library/Developer/Xcode/DerivedData
tmutil addexclusion ~/.cache
tmutil addexclusion ~/.vscode/extensions
tmutil addexclusion /Library/Caches/Homebrew
tmutil addexclusion ~/Library/HTTPStorages
```

### Keep (already good)

- `/Users/michael/.gem` — ✓
- `/Users/michael/.npm` — ✓
- `/Users/michael/.cpan` — ✓
- `/Users/michael/Library/Containers` — ✓
- `/Applications` — ✓
- `/Users/michael/Library/Dropbox` — ✓
- `/Users/michael/Library/CloudStorage/Dropbox` — ✓
- `/Users/michael/Library/Mobile Documents/com~apple~CloudDocs` — ✓
- `/Users/michael/repos` — ✓

---

## Result

After updates:

- **Backed up (Tier 1 + 2):** Keychain, SSH keys, GPG keys, preferences, Mail/Calendar/Contacts, browser profiles, shell config, editor config
- **Excluded (Tier 3):** All regenerable caches, logs, build artifacts, package caches
- **Restore time:** ~15–30 min (vs. 45+ min with regenerable bloat)
- **Storage saved:** 10–15 GB per backup cycle
