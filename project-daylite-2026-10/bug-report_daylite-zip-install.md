# Bug report: Daylite install from latest-daylite.zip

## Summary

The Marketcircle download is a `.zip` containing a notarized Mac app. Launching it from `~/Downloads` runs it from App Translocation. Moving the original afterward leaves the running app in a state where it reports it is "running from its original download location" and asks to be moved. The install works, but only after an extra quit-and-relaunch that the instructions don't mention. The instructions also require moving the app with Finder, and never say so.

## Environment

- macOS Darwin 25.6.0
- Download: `latest-daylite.zip`, 107 MB compressed, 283 MB uncompressed, 4,747 files
- App: Daylite 2026.42.0 (build 22049), min macOS 15.2
- Signed: Developer ID Application, Marketcircle Inc (GR26KTJYTV), notarized; `spctl` accepts it

## Reporter context

- Power user. Works in the shell and in Emacs, and avoids point-and-click for file operations.
- Moved the app with Emacs Dired first, then with `mv(1)` in bash, then with Finder. The instructions said only to move `Daylite.app` from `~/Downloads` to the `/Applications` directory.
- Nothing in the instructions said Finder was required, or that `mv(1)` or Dired would fail or leave the app in a bad state. Each method appeared to succeed.

## Steps and observations

1. Opened <https://www.daylite.app/downloads/> and downloaded <https://www.daylite.app/appcasts/releases/latest-daylite.zip> to `~/Downloads/latest-daylite.zip`. The file name gives no version. The versioned file the appcast points to is `daylitedma-releases-2026.42.0.b22049.2026-10-20-1048.zip`.
2. Double-clicked `~/Downloads/latest-daylite.zip` in Finder. It expanded to `~/Downloads/Daylite.app`.
3. Opened `Daylite.app` from `~/Downloads`. Gatekeeper prompt accepted. App launched from its download location.
4. Moved `~/Downloads/Daylite.app` to `/Applications/Daylite.app`. Reported method: Finder drag. Also tried `mv` and Emacs Dired; results below.
5. Ran `open /Applications/Daylite.app`. Result: a dialog titled "Move Daylite to the Applications Folder", saying the app "is running from its original download location and won't be able to update itself," with a "Quit Daylite" button.
6. The running process was the translocated copy under `/private/var/folders/.../AppTranslocation/.../Daylite.app`, which is read-only. It still showed the dialog after the original was moved.

## Expected

The "Move to Applications" prompt should not appear after the app is in `/Applications`, or the instructions should say to quit before moving.

## Root cause

- Launching a quarantined app from `~/Downloads` makes macOS run a read-only copy from a randomized AppTranslocation path.
- Moving the original does not change the running copy. The app then reports the original location and asks to be moved.
- Finder, `mv`, and Dired all rename the same file on the same volume. The difference is which copy is running, not how the file was moved.

## Distribution

- The archive format is `.zip`. A notarized Mac app is normally distributed as a `.dmg` with an `Applications` link, so the user drags the app into `/Applications` before launching. That's the standard Mac process, and the `.zip` is not.
- The instructions depend on launching from Downloads and then moving, which triggers translocation.
- The instructions require moving the app to `/Applications` with Finder. They never say that, and they say nothing about what happens if the app is launched first. Finding this out cost a reinstall attempt, and it leaves the app in a state the instructions don't cover.
- Shipping a Mac-only app as a `.zip` with a Finder-only install step is the wrong format for macOS.

## Implications of a non-standard Mac install

- Updates: the app says it "won't be able to update itself" from the translocated location. Automatic updates fail until the app is moved, so users stay on old versions without knowing it.
- Support: the install needs a Finder move and a second launch that no instruction mentions. Each user who hits this either writes to support or gives up.
- Automation: `.zip` and drag-to-Finder installs can't be scripted, deployed by MDM, or installed by Homebrew the way a `.dmg` or `.pkg` can. Every Mac that gets Daylite needs hands-on setup.
- Reproducibility: a manual, order-dependent install makes machine setup hard to repeat and verify across machines.
- Mac users expect the drag-to-Applications pattern. A zip that depends on the user doing a Finder move undercuts the platform the app is built for.

## Table: how the app was moved

| Method      | Moved the file | Works from /Applications | Notes                                                                                                                                                              |
|-------------|----------------|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Finder drag | Yes            | Yes                      | User reports it opened from /Applications with helper announcements.                                                                                               |
| `mv(1)`     | Yes            | Not confirmed            | `/Applications/Daylite.app` exists and is valid (2026.42.0, Gatekeeper accepted). The `open` after `mv` activated the translocated instance and showed the dialog. |
| Emacs Dired | Yes            | Not confirmed            | User reports Daylite did not notice the move. Same translocated-instance cause as `mv`.                                                                            |

## Requested fixes

1. Ship a standard `.dmg` with an Applications shortcut. This is the fix requested. Replace the `.zip` rather than adding alongside it.
2. Until then, if the `.zip` stays, state in the instructions that `Daylite.app` must be moved to `/Applications` with Finder before the first launch, and must not be opened from Downloads.
3. Name the file with the version number, for example `daylitedma-releases-2026.42.0.b22049.dmg`, and link it from <https://www.daylite.app/downloads/>.
