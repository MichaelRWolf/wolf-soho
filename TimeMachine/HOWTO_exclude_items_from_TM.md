# Excluding items from Time Machine

## How to display excluded items

### GUI

**System Settings → General → Time Machine → Options** (or **System Preferences → Time Machine → Options** on older macOS). The list under "Exclude these items from backup" is your exclusion list.

### Command line: read the preference plist

User exclusions are stored in **SkipPaths**; some system-wide exclusions in **ExcludeByPath**:

```bash
defaults read /Library/Preferences/com.apple.TimeMachine SkipPaths
defaults read /Library/Preferences/com.apple.TimeMachine ExcludeByPath
```

Full plist (paths and other TM settings):

```bash
plutil -p /Library/Preferences/com.apple.TimeMachine.plist
```

### Command line: check whether a path is excluded

```bash
tmutil isexcluded /Users/michael/Downloads
# [Excluded]  /Users/michael/Downloads
# or
# [Included]  /Users/michael/Downloads
```

There is no `tmutil` verb to list all excluded paths; use the plist above.

---

## Valuable for future restore (keep in backup)

Worth keeping in Time Machine so restore actually helps:

| Path | Why |
|------|-----|
| `~/Library/Preferences` | App settings, key bindings, window state. Small, often portable. |
| `~/Library/Fonts` | User-installed fonts. |
| `~/Library/Keychains` | Passwords, certs (restore can need re-auth). |
| `~/Library/LaunchAgents` | Custom user launch agents. |
| `~/Documents` | Your documents (unless elsewhere/synced). |
| `~/Desktop` | Desktop contents. |

Optional (only if you rely on local data):

| Path | Why |
|------|-----|
| `~/Library/Mail` | Only if you use local mail (POP, local mailboxes). |
| `~/Library/Messages` | Only if you want iMessage history/attachments restored (large). |
| `~/Library/Safari` | Often redundant if Safari is synced via iCloud. |

---

## Useless and/or fragile to future restore (exclude)

Large, rebuildable, or restore-unfriendly. Excluding saves space and backup time; restore is rarely useful or safe.

| Path | Why |
|------|-----|
| `~/Library/Application Support` | App caches, state, cruft. Restore is fragile or ignored. |
| `~/Library/Containers` | Sandboxed app data. Same story. |
| `~/Library/Group Containers` | App-group shared data. Same story; often larger. |
| `~/Library/Caches` | Cache. Rebuildable. (Newer macOS may skip by default.) |
| `~/Library/Logs` | Logs. (Newer macOS may skip by default.) |
| `~/Library/Developer` | Xcode, simulators, derived data. Rebuildable. |
| `~/Library/CloudStorage` | Synced (Dropbox, iCloud, etc.). |
| `~/Library/Mobile Documents/com~apple~CloudDocs` | iCloud Drive. |
| `~/Downloads` | Ephemeral. |
| `~/.Trash` | Trash. |
| `~/.gem` `~/.npm` `~/.cpan` | Dev package caches. Reinstall with one command. |
| `~/.cursor` `~/.local` | Editor/tool caches and state. Rebuildable. |
| `~/Pictures` | If you use iCloud Photos or back up photos elsewhere. |
| `/Applications` | Reinstall from App Store or installers. |
| `~/repos` | Git clone again. |

---

## Bash: set the exclusion list (no clicky-clicky)

Adding one path (sticky; survives move/rename):

```bash
tmutil addexclusion /Users/michael/Library/Group\ Containers
```

Removing one path:

```bash
tmutil removeexclusion /Users/michael/Library/Group\ Containers
```

Setting the full SkipPaths list at once (replace the array with your paths). **Requires root** because the plist is in `/Library/Preferences`:

```bash
sudo defaults write /Library/Preferences/com.apple.TimeMachine SkipPaths -array \
  "/Users/michael/Pictures" \
  "/Users/michael/Library/Application Support" \
  "/Users/michael/Library/Containers" \
  "/Users/michael/Library/Group Containers" \
  "/Users/michael/Library/CloudStorage" \
  "/Users/michael/Library/Mobile Documents/com~apple~CloudDocs" \
  "/Users/michael/Downloads" \
  "/Users/michael/.Trash" \
  "/Users/michael/.gem" \
  "/Users/michael/.npm" \
  "/Users/michael/.cpan" \
  "/Users/michael/.cursor" \
  "/Users/michael/.local" \
  "/Applications" \
  "/Users/michael/repos" \
  "/Users/michael/Library/Application Support/Google"
```

Then either wait for the next backup or toggle Time Machine off and on so it reloads the plist.

To append one path without replacing the whole list, use `tmutil addexclusion` (no sudo).

---

## Verify exclusions (TAP script)

From the **TimeMachine** directory, **verify-tm-isexcluded** checks that paths in `tm-exclude-include.yaml` match TM state and outputs TAP. It does not change any settings.

**Stand-alone:**

```bash
cd TimeMachine
./verify-tm-isexcluded
./verify-tm-isexcluded path/to/tm-exclude-include.yaml
```

**With a test runner (e.g. prove):**

```bash
cd TimeMachine
prove ./verify-tm-isexcluded
./verify-tm-isexcluded | prove -
```

YAML lists: `must_include` (paths that must be included) and `must_exclude` (paths that must be excluded). Edit the YAML in the same directory as the script to match your desired policy.

---

## ExcludeByPath (system-wide)

System-wide exclusions (e.g. `/Library/Application Support/Microsoft/PlayReady`) are in **ExcludeByPath**. Edit the plist with care; those are often set by installers or admin preference. To only inspect:

```bash
defaults read /Library/Preferences/com.apple.TimeMachine ExcludeByPath
```
