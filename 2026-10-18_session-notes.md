# 2026-10-18 Session Notes: Intel Binary Cleanup on michael-air

## Problem

Migration Assistant copied Intel-only (x86_64) binaries from michael-pro onto michael-air (Apple Silicon) without warning. They fail one by one with `Bad CPU type in executable`. Tracked in GitHub issue #8.

## Detection

Run the audit (read-only, about 1.5 minutes for the full default scan):

```bash
x86-audit                      # default locations, expected files hidden
x86-audit --all                # include allowlisted (expected) files
x86-audit --out ~/x86.tsv DIR  # scan DIR and save the report
```

Check a single file:

```bash
lipo -archs /path/to/binary
```

Output for an Intel-only file:

```text
x86_64
```

## Tool Built: `bin/x86-audit`

- Reports Mach-O files that contain x86_64 and lack arm64. Universal binaries are not reported.
- Handles fat binaries per slice (`file` prints one line per architecture).
- Uses BSD `find -perm +111`; macOS `find` has no `-executable`, so the search commands originally in #8 do not work.
- Sets `LC_ALL=C`, because `file` output can contain non-UTF-8 bytes that crash `awk`.
- Allowlist hides expected Intel slices: Emacs per-arch dirs, Chrome Widevine, Typora, Homebrew test fixtures, python.org `-intel64` launchers, Apple Command Line Tools, `/Library/Apple`.
- Default scan: `/usr/local`, `/opt`, `/Applications`, `/Library`, `~/Library`, `~/bin`, `~/repos`, and the `~` dotdirs.

## Commits

- `8f2957b` Add x86-audit: find Intel-only binaries (#8)
- `5c245b6` x86-audit: scan /Library and ~/Library by default (closes #8)

All changes: <https://github.com/MichaelRWolf/wolf-soho/compare/1bbcdbb...5c245b6>

## Removed

Everything was moved to the Trash (`trash` / `sudo trash`) so it can be restored.

| Area             | Removed                                                                                                 |
|------------------|---------------------------------------------------------------------------------------------------------|
| Python           | python.org 3.7, 3.10, 3.12, 3.13; pipx `flent` venv; `~/bin/venv`; orphaned `m_and_m_hungarian` venv    |
| Python (rebuilt) | `~/Library/Python/3.12` packages reinstalled as ARM: contourpy, fonttools, kiwisolver, matplotlib       |
| Java             | Temurin 11, OpenJDK 18                                                                                  |
| ODBC             | Redshift, Simba SQL Server, Simba Spark; dead PostgreSQL entry; both `odbcinst.ini` files               |
| Printers         | HP, Epson, Lexmark, Brother drivers (all printers use AirPrint)                                         |
| Scanners         | Epson, HP, Neat, Brother, Canon Image Capture drivers                                                   |
| Kernel ext.      | DuetDisplay, HighPoint (2), Plantronics, SoftRAID, old Google Drive `dfsfuse`                           |
| Helpers          | GitHub CLI installer (stale Intel copy), Telestream licensing, Google Drive icon, FLEXnet licensing     |
| Launch jobs      | GitHub CLI installer, Telestream licensing, MySQL `mysqld`                                              |
| Plug-ins         | NPAPI browser plug-ins, Address Book, QuickLook, Automator, InterCall Chrome host, Neat PDF Services    |
| Audio            | Telestream audio capture driver                                                                         |
| Apps             | SynologyAssistant; Daylite Server 4 program and logs (database `Storage.dlsdb` kept)                    |
| Perl / Ruby      | Perl 5.18, 5.30; two Perl 5.34 XS modules; Intel nokogiri gem; stale `racc` build (racc rebuilt as ARM) |
| Other            | MySQL pref pane, Dropbox helper tools, Audacity and OBS leftovers                                       |
| Caches           | Cursor agent versions, Puppeteer Chrome 127 x64                                                         |

## Kept on Purpose

- Zoom audio driver: in use.
- Apple-managed: Command Line Tools, CoreSimulator, MRT.
- Small optional pieces: Discord SDK, Quicksilver actions, gcloud `crcmod`, Codex `reflink`.

## GitHub

- #8: closed by `5c245b6`; summary comment with commit list.
- #6, #9, #10: progress comments; the `#6` label fixed in #8, #9, #10 to "michael-air setup and configuration".

## How-To: Start a Live-Notes Agent Session Again

Live-notes tool by Nitsan (from today's Approval Tests session). Permissions for agents may change on his side.

1. In the Meetings host app, start a note and copy its **agent link** (`https://live-notes-sdk-production.up.railway.app/a/<token>/`). Keep it private.
2. In Claude Code, cd to the repo you want to work in and choose the permission mode:
   - **Manual**: approve each call.
   - **Bypass**: no prompts. Needed for voice-requested deletions and page writes; auto mode blocks them.
3. Pick the model: `/model` → Opus 5.5.
4. Paste this prompt, with your link:

   ```text
   Please join this conversation and follow it live: <agent-link>
   I appear in it as Michael R. Wolf. Act on my requests, spoken or typed. Respond only on your attention page in the meeting (your responses, results and questions).
   Use the connection instructions and follower supplied by the link. Before you publish your page, read <agent-link>patterns (the solo section).
   ```

5. Claude fetches the guide, downloads `follow.mjs`, starts it under Monitor, and publishes the attention page. Watch for `! live: following this note as michael-claude`.
6. Talk. Requests go on the page under **Now**, **Tasks** and **For you**. Reply by voice with the exact phrases the page suggests.
7. If the follower stops (30-minute Monitor limit), Claude reruns the same command; the `--state` cursor file resumes in place.
8. A note ends after its lifetime cap, 3 hours by default. To continue, start a new note and paste its new link; the page has to be republished there.

## How the Session Ran: Live Notes + Claude Code

The work was driven by voice from a live meeting note, not typed prompts.

```text
 Michael (voice/chat)
        │
        ▼
 Live note (Meetings host app, live-notes-sdk-production.up.railway.app)
        │  speech → text events (feed / SSE stream)
        ▼
 follow.mjs (Node follower, run under Claude Code's Monitor tool)
        │  one line per event → delivered into the Claude Code session
        ▼
 Claude Code agent "michael-claude" (Opus 5.5, in ~/repos/wolf-soho)
        │  acts: shell, gh, git, edits
        ▼
 Attention page (Markdown, PUT pages/michael-claude[/sub-page])
        │  Now / Tasks / For you; tabs = sub-pages
        ▼
 Michael reads results in the note
```

- **Join:** the owner pastes the note's agent link into Claude Code. The link serves a Markdown guide: rules, routes, and the follower script.
- **Name:** `<owner>-<runtime>`, so `michael-claude`. Every request carries `?name=michael-claude`.
- **Follower:** `follow.mjs` handles reconnects, keeps a cursor in a `--state` file, skips the agent's own lines, and joins speech fragments. Monitor expires after 30 minutes; rerun the same command and the cursor file resumes without replaying history.
- **Page:** the first `PUT` returns an owner key; every later write sends it as `X-Agent-Key`. Sub-pages ("tabs") are `PUT`/`DELETE pages/michael-claude/<path>`. Readers see changes live.
- **Scope:** only the owner's lines are requests; other speech in the room is data. Ambiguous lines got a question on the page instead of action.
- **Security:** the agent link is a secret (it can post, publish and revoke). Share only the read-only view link.
- **Permissions:** in Claude Code auto mode, the classifier blocked the follower download, page writes, and deletions requested by voice. Manual mode, and later bypass mode, let the session proceed. Removals used `trash`, so they can be undone.

## Lessons

- Scope audits to the whole disk from the start. `/Library` is readable without sudo; skipping it hid about 700 files until the last pass.
- Check how printers are configured before removing drivers: `grep NickName /etc/cups/ppd/*.ppd` shows `-AirPrint` when vendor drivers are unused.
- Auto mode blocks deletions and outbound writes requested by voice; Manual or bypass mode was needed to act on meeting requests.

## Follow-up

- [ ] Reboot so the removed kernel extensions are fully dropped.
- [ ] Rerun `x86-audit` after any future Migration Assistant restore (see #9).
- [ ] Empty the Trash before sizing michael-air's Time Machine backups (see #10).
