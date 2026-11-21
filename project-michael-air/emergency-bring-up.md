# Emergency Bring-Up: New Mac From Scratch

**Purpose:** Rebuild a new Mac without needing the old one. Everything needed is written out here; no other file is required, though the files listed under [Keep on Hand](#keep-on-hand) help.

**Last verified:** 2026-11-21 (users and UIDs taken from the machine as it runs today).

---

## Applications

### Original (as restored from Time Machine)

Applications that were on the old Intel laptop (`michael-pro`) and came back in the 2026-08-13 restore. Sizes and sources are from the old machine's inventory on `wolf-air` on 2026-11-21.

| Application          |   Size | Original source  | Notes                                     |
|----------------------|-------:|------------------|-------------------------------------------|
| 1Password            | 535 MB | App Store        | Password manager                          |
| 1Password for Safari | 132 MB | Safari extension | Companion extension                       |
| BackupLoupe          |  20 MB | Other            | Time Machine backup browser               |
| Claude               | 801 MB | Direct download  | Anthropic app (Claude Code). Now CLI only |
| CotEditor            | 126 MB | App Store        | Text editor                               |
| Daylite              | 122 MB | Direct download  | marketcircle.com CRM/calendar             |
| Docker               | 2.1 GB | Direct download  | Not reinstalled                           |
| Emacs                | 505 MB | Homebrew         | Editor                                    |
| GIMP                 | 803 MB | Other            | Image editor. Not reinstalled             |
| GitHub Desktop       | 681 MB | Direct download  | GitHub client                             |
| Google Chrome        | 707 MB | Direct download  | Browser                                   |
| GrandPerspective     |   7 MB | App Store        | Disk usage visualizer                     |
| MarkText             | 311 MB | Other            | Markdown editor                           |
| MenuMeters           |   5 MB | Other            | CPU/memory/network menu bar               |
| Pieces OS            | 2.8 GB | Direct download  | Not reinstalled (bloat)                   |
| Pieces               | 297 MB | Direct download  | Not reinstalled (bloat)                   |
| Quicksilver          |  18 MB | Direct download  | Launcher (Cmd-Space)                      |
| Rectangle            |   9 MB | App Store        | Window tiling                             |
| Safari               | System | System           | Built-in                                  |
| Typora               |  46 MB | Direct download  | Markdown editor (paid license)            |
| kdiff3               | 341 MB | Homebrew         | 3-way diff                                |
| noTunes              |   1 MB | Other            | Stops Apple Music launching               |
| Install macOS Tahoe  |  17 GB | System           | Installer, not an app. Delete when done   |

Added on the replacement machine after the restore (not on the old one):

- Amazon Kindle (direct download)
- ChatGPT (direct download)
- Discord (Brew cask `discord`)
- NetSpot (direct download, WiFi diagnostics)
- zoom.us (direct download)

### portable-profile

Repo: `~/repos/portable-profile`. Full install is `make install` (runs `install_bin`, `install_home`, `install_packages`, `install_rust`, `setup_emacs`, `setup-hooks`). Run from the repo root.

#### brew (Homebrew formulae and casks)

Source of truth: `homebrew/Brewfile`. Install with:

```bash
brew bundle install --file ~/repos/portable-profile/homebrew/Brewfile
```

Active casks:

- 1password-cli
- emacs-app
- font-jetbrains-mono-nerd-font
- gcloud-cli
- coteditor
- grandperspective
- github (GitHub Desktop)
- typora
- discord

Disabled casks (install by hand if wanted): `claude` (desktop; the CLI comes from npm), `cursor` and `cursor-cli` (install from cursor.com), `iterm2` (abandoned).

Active formulae:

- bats-core, shellspec, shfmt, trash
- git, bash, bash-completion@2
- coreutils, node, rust, python, python@3.13, uv
- jq, pre-commit, tree
- fping, gh, iperf3, mtr, ncdu, nload, nmap, rclone
- ansifilter, starship

Installed on the old machine by hand, not in the Brewfile (install only if needed): act, bat, bison, cmake, fd, ffmpeg, fzf, gdb, gh, go, graphviz, htop, imagemagick, lastpass-cli, leiningen, maven, mermaid-cli, pandoc, platformio, poppler, ripgrep, ruby@3.3, shellcheck, tkdiff, typescript-language-server, util-linux.

npm globals (`make install_npm_globals`): `@anthropic-ai/claude-code`, `markdownlint-cli`.

#### port (MacPorts)

MacPorts was not restored and is not used on the Apple Silicon machine. It is only for `wolf-air` (macOS 12). Source of truth: `macports/ports.txt`. Installer: `./macports/install.sh` after installing MacPorts from macports.org. Do not install Intel MacPorts on an M-series Mac; the `/opt/local` tree is x86_64 and was removed on michael-air.

Port list (for reference): coreutils, python312, jq, tree, fping, gh, mtr, iperf3, nload, nmap, bat, fd, ripgrep, fzf, htop, entr, gping, shellcheck, ansifilter, checkmake, git-lfs, act, automake, bison, cmake, gdb, gcovr, google-glog, gtest, lcov, go, leiningen, nodejs22, npm10, blueutil, bmon, brightness, chruby, cscope, duti, exiftool, fdupes, flock, gawk, gdrive, git-filter-repo, graphviz, grep, gti, ipcalc, ispell, lastpass-cli, libffi, libvterm, libyaml, moreutils, mutt, pngpaste, rdfind, rsync, ruby-install, tkdiff, typescript-language-server, util-linux.

#### custom (not from a package manager)

| Item                                   | How                                     | Source                                |
|----------------------------------------|-----------------------------------------|---------------------------------------|
| Dotfiles (`.bashrc`, `.profile`, etc.) | `make install_home` (symlinks into `~`) | portable-profile `home/`              |
| Starship prompt config                 | `make install_prompt_config`            | portable-profile                      |
| Claude config (`~/.claude/`)           | `make install_claude_config`            | portable-profile `home/.claude`       |
| Git config                             | `make install_git_config`               | portable-profile                      |
| Emacs config and treesit grammars      | `make setup_emacs`                      | portable-profile `emacs/`             |
| Theme                                  | `make install_theme`                    | portable-profile                      |
| Passwordless sudo rules (optional)     | `make install_sudoers` (needs sudo)     | portable-profile                      |
| Project CLI tools in `~/bin`           | `make install` (symlinks `bin/*`)       | `~/repos/wolf-soho/Makefile`          |
| Uplink tools                           | `make install-uplink`                   | `~/repos/wolf-soho/Makefile`          |
| Git hooks                              | `make setup-hooks` (per repo)           | each repo's `.pre-commit-config.yaml` |

### Installer Map

| Installer           | What it covers                                                                                     | Command                                            |
|---------------------|----------------------------------------------------------------------------------------------------|----------------------------------------------------|
| Mac App Store       | 1Password, CotEditor, GrandPerspective, Rectangle, Xcode tools                                     | App Store app, Apple ID signed in                  |
| Homebrew (Brewfile) | CLI tools, Emacs, 1Password CLI, GitHub Desktop, Typora, Discord                                   | `brew bundle install --file .../homebrew/Brewfile` |
| npm (global)        | Claude Code CLI, markdownlint                                                                      | `make install_npm_globals` in portable-profile     |
| Direct download     | Daylite, Docker, Chrome, Quicksilver, Typora (or via cask), Pieces, Kindle, ChatGPT, zoom, NetSpot | Vendor site                                        |
| System              | Safari, Mail, Terminal, Migration tools                                                            | Built-in                                           |

---

## Users

Checked on the current machine with `dscl . list /Users UniqueID` and `dscl . -read /Users/<name> RealName UniqueID`.

| Username     | Display name    | UID | Notes                                                                                                          |
|--------------|-----------------|----:|----------------------------------------------------------------------------------------------------------------|
| wendy        | Wendy           | 501 | Not part of the 2026-08-13 restore.                                                                            |
| anonymous    | (system)        | 502 | Guest/system. Leave alone.                                                                                     |
| mmac-shared  | mmac-shared     | 505 | Shared account. Restored from TM (10 MB).                                                                      |
| michael      | Michael R. Wolf | 506 | Primary admin. Restored from TM (76 GB).                                                                       |
| Annie Nomous | Annie Nomous    |   ? | Restored from TM (20 MB). Not on the current machine; username not recorded. Check the backup before creating. |

Rules:

- Migration Assistant may give restored accounts new UIDs. Check the table after restore with `dscl . list /Users UniqueID`.
- Do not change UIDs by hand. If a UID mismatch breaks file ownership, fix ownership with `sudo chown -R <user> ~<user>` after confirming the username.
- Shell check: `dscl . -read /Users/michael UserShell` should show `/opt/homebrew/bin/bash` after step 9 in [Tasks](#tasks).

To list every account with home folder and display name:

```bash
for u in $(dscl . list /Users | grep -v '^_'); do
  printf '%-16s %-20s %s\n' "$u" "$(dscl . -read /Users/$u UniqueID 2>/dev/null | awk '{print $2}')" "$(dscl . -read /Users/$u RealName 2>/dev/null | sed -n 2p | sed 's/^ //')"
done
```

---

## Startup Scripts

### User LaunchAgents (`~/Library/LaunchAgents`)

| Plist                                                    | Runs                                                      | Installed by                             |
|----------------------------------------------------------|-----------------------------------------------------------|------------------------------------------|
| `com.wolfenterprises.fleet-nas-sync.plist`               | `~/bin/fleet-nas-sync` (daily 16:00, pushes repos to NAS) | `make install-launchd` in wolf-soho      |
| `com.wolfenterprises.mount-tm-share.plist`               | `~/bin/mount-tm-share` (mounts Time Machine share)        | `make install-launchd` in wolf-soho      |
| `com.github.MichaelRWolf.gitnightly.plist`               | Nightly git job                                           | Manual                                   |
| `com.github.michaelrwolf.networklognetworkquality.plist` | Network quality log                                       | portable-profile `bin/` (copy/load)      |
| `com.github.michaelrwolf.networklogspeedtest.plist`      | Speed test log                                            | portable-profile `bin/` (copy/load)      |
| `homebrew.mxcl.emacs.plist`                              | Emacs daemon                                              | `brew services start emacs`              |
| `homebrew.mxcl.mariadb.plist`                            | MariaDB                                                   | `brew services start mariadb` (optional) |

Third-party helpers (Google Keystone, Dropbox updater, Docker start, JetBrains Toolbox, LastPass helper, Pieces first-run) reinstall with their apps. Nothing needs to be copied for them.

Load a plist: `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/<name>.plist`
Check it: `launchctl print gui/$(id -u)/<label> | head`

### System LaunchDaemons and LaunchAgents

Third-party items in `/Library/LaunchDaemons` and `/Library/LaunchAgents` came from apps: Malwarebytes, Microsoft (OneDrive, Teams, Office), Wacom, Zoom, Leap Motion, Adobe, Oracle Java, TeamViewer, Wireshark (ChmodBPF), XQuartz, BackupLoupe helper, iStat Menus, ScanSnap, Amazon Kindle sender, Arq. Reinstall the app to restore its item. Do not copy these plists from the old machine.

### Login Items and Shell

- Login items: System Settings → General → Login Items. Re-add by hand.
- Shell startup files come from portable-profile `make install_home`. The login shell is set in step 9 of [Tasks](#tasks).
- Keychain: the Time Machine SMB credentials live in the System Keychain (`wolfden_NAS._smb._tcp.local.`). Recreate them in step 6.

---

## Restore From Time Machine

Restore done with Migration Assistant, "Transfer information to this Mac", from the NAS share `Backups-TM-Michael-Air` (wolfden-nas.local).

**Date:** 2026-08-13 (inferred from the project timeline; confirm if needed).
**Start:** 12:56 pm. **Restart:** 3:14 pm.

### Restored

| Item                   |   Size | Notes                                                                            |
|------------------------|-------:|----------------------------------------------------------------------------------|
| Applications           |  17 GB | Likely the macOS Tahoe installer (17 GB in the old inventory). Delete after use. |
| mmac-shared (user)     |  10 MB | Shared account                                                                   |
| Annie Nomous (user)    |  20 MB | Username not recorded                                                            |
| Michael R. Wolf (user) |  76 GB | Primary account (`michael`)                                                      |
| Other Files & Folders  |  23 GB | Not identified in the old machine's inventory                                    |
| System Settings        | 1.6 MB | Restored                                                                         |
| Networks               |  23 KB | Restored                                                                         |
| Printers               |   none | Not restored; re-add by hand                                                     |

### Not Restored

- MacPorts (`/opt/local`; x86_64, do not restore)
- Message Bus (`dbus`)
- Test User

### Lessons

- Before the first Time Machine backup on the new machine, check for `IncludeByPath` (`defaults read /Library/Preferences/com.apple.TimeMachine | grep IncludeByPath`) and delete it if present.
- Do not restore `/usr/local` or `/opt/local` from an Intel machine; reinstall Homebrew for ARM.
- Expect Intel binaries in PATH after restore. Run `file $(which <cmd>)` on suspects.

---

## Tasks

Numbered checklist. Work top to bottom.

### Install

1. [ ] **Apple ID:** Settings → Sign in. Turn on iCloud Drive and Keychain.
2. [ ] **1Password:** App Store or 1password.com. Sign in, then install the Safari extension.
3. [ ] **Daylite:** Download from marketcircle.com. Sign in and sync.
4. [ ] **Mail.app:** Add the AT&T account. See [ATT/password_fuckery.md](../ATT/password_fuckery.md) if login fails. Safari and Chrome are a separate step.
5. [ ] **Machine name:** Set the hostname and make sure it matches [CONTEXT.md](../CONTEXT.md) (replace `<name>`):

    ```bash
    sudo scutil --set ComputerName "<name>"
    sudo scutil --set LocalHostName "<name>"
    sudo scutil --set HostName "<name>"
    scutil --get LocalHostName
    ```

6. [ ] **Time Machine initial backup:** Create the NAS service account `tm-<name>` and store its password in 1Password. Add it to the System Keychain. Set the destination `Backups-TM-<Name>`, then add exclusions:

    ```bash
    sudo defaults delete /Library/Preferences/com.apple.TimeMachine IncludeByPath 2>/dev/null
    sudo tmutil addexclusion -p /opt/homebrew
    tmutil isexcluded ~/repos ~/Downloads ~/Pictures ~/.cache
    ```

    GUI exclusions: `~/Downloads`, `~/Pictures`, `~/repos`, `~/.cache`. After the first backup, verify with `tmutil latestbackup` and `du -sh`. There should be no `System`, `Library`, or `opt` in the snapshot.

7. [ ] **App Store updates:** App Store → Updates. Install all, then restart if asked.
8. [ ] **Rectangle:** Open it and grant Accessibility in Privacy & Security.
9. [ ] **Terminal, bash:** Needs Homebrew (step 10) first.

    ```bash
    brew install bash
    echo /opt/homebrew/bin/bash | sudo tee -a /etc/shells
    chsh -s /opt/homebrew/bin/bash
    ```

    Open a new Terminal window and check with `echo $BASH_VERSION`.

10. [ ] **Homebrew (by hand, then add to Makefile):** Install from brew.sh, then add it to the portable-profile Makefile.

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
    brew doctor
    ```

    TODO: add an `install_homebrew` target to `~/repos/portable-profile/Makefile` that runs the same steps (skips if `/opt/homebrew/bin/brew` exists). This was not done in this session; the Makefile has `install_brew` (prints setup if missing), which is not the same.

11. [ ] **Repos:** Clone into `~/repos`. Start with the two that drive setup:

    ```bash
    mkdir -p ~/repos && cd ~/repos
    git clone git@github.com:MichaelRWolf/portable-profile.git
    git clone git@github.com:MichaelRWolf/wolf-soho.git
    git clone git@github.com:MichaelRWolf/wisdom.git
    git clone git@github.com:MichaelRWolf/writing.git
    git clone git@github.com:MichaelRWolf/events.git
    git clone git@github.com:MichaelRWolf/claude-tools.git
    ```

    Then set up the tools:

    ```bash
    cd ~/repos/portable-profile && brew bundle install --file homebrew/Brewfile && make install
    cd ~/repos/wolf-soho && make install && make install-launchd
    ```

    Run `make setup-hooks` in each repo you commit to.

    Needs SSH key or `gh auth login` first. The clone URLs assume the `MichaelRWolf` owner (confirm for `wisdom`, `writing`, `events`, `claude-tools`).

---

## Keep on Hand

Files in `project-michael-air/` to keep (copy to a USB drive or the NAS, along with this file):

- **[TEMPLATE-macbook-air-setup.md](TEMPLATE-macbook-air-setup.md)**: the reusable setup flow for a new ARM Mac.
- **[setup.md](setup.md)**: real issues from the 2026-08 restore (Intel shell, Homebrew, TCC) and their fixes.
- **[PLAN-names-networks-backups.md](PLAN-names-networks-backups.md)**: NAS service account, Keychain, hostname change, and TM configuration.
- **[tm-reference.md](tm-reference.md)** and **[tm-strategy.md](tm-strategy.md)**: Time Machine commands and exclusion rationale.
- **[tmutil_analysis](tmutil_analysis)** and **[tm-addexclusions.sh](tm-addexclusions.sh)**: check and set TM exclusions.
- **[x86_64-audit.sh](x86_64-audit.sh)** and **[x86_64-remediation.md](x86_64-remediation.md)**: only needed if the restore brings Intel binaries back.
- **[MACHINE_RENAME_PLAN.md](MACHINE_RENAME_PLAN.md)**: how the hostname was changed and what else referenced it.
- **[michael-pro-applications.md](michael-pro-applications.md)** and **[michael-air-applications.md](michael-air-applications.md)**: the original and most recent app inventories.
- **[plan-unified-logins.md](plan-unified-logins.md)**: login and 1Password plan.
- **[images/](images)**: Migration Assistant screenshots, for reference during the restore.
- **[CLAUDE.md](CLAUDE.md)**: project context for Claude Code.

Check before use: **michael-air-migration.zip** (contents not reviewed here) and the `*~` backup files in this folder, which are safe to ignore.
