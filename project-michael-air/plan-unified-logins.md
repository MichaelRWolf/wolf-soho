# Plan: Unified logins across michael-air, wolf-air, wendy-air

## Goals

1. **Prove out a unified-login architecture** where each person (michael, wendy) has consistent
   logins across multiple machines, so machine choice becomes incidental to daily work rather
   than a constraint (the "machine shouldn't matter" model).
2. **Start with wendy as proof-of-concept** by giving her a real, consistent login on all
   three machines (wolf-air + michael-air + eventual wendy-air), testable with the interim
   setup described below.
3. **Make identity and personal data portable** via unified Apple ID sign-in + iCloud sync
   (Safari, Documents, Keychain), so her work state and content follow her across machines,
   not locked to one device.
4. **Establish repeatable patterns** for UID consistency, account provisioning, and iCloud
   configuration that can be applied to michael's accounts once this pattern proves stable.
5. **Bridge to wendy-air's future arrival** by giving her interim borrowed-compute access
   on michael-air (for RAM/CPU-heavy work like Zoom) while her day-to-day base stays on
   wolf-air, until wendy-air (the hand-down of michael-air once you migrate to michael-air2)
   actually exists, at which point wolf-air retires.
6. **Enable multi-machine flexibility** for specialized workflows -- e.g., two-machine Zoom
   setups (one for camera/people, one for screen-share/reference) become natural once both
   people have unified logins everywhere.

## Context

Both `michael-pro` (water damage, 2026-06-18) and `wendy-pro` (water damage, 2026-08-03) are
dead. The recorded recovery path (`project-wendy-air/`, decided 2026-08-29) hands down the
*current* michael-air to Wendy (renamed `wendy-air`) once Michael upgrades to a
`michael-air2` -- still pending purchase. `wolf-air` (2015 MacBookAir7,2, Monterey, EOL, no
Touch ID) is Wendy's interim home base but was independently assessed
(`wendy-options.md`) as not viable beyond ~3 months.

This plan establishes a **unified-login architecture** as an interim test before committing
to the long-term pattern. By adding consistent wendy accounts across all three machines
(wolf-air, michael-air, eventual wendy-air), we can evaluate whether "the machine doesn't
matter" actually works in practice -- can she seamlessly switch between them for different
workloads (slow work on wolf-air, compute-heavy on michael-air/wendy-air) without friction?
If this pans out, the same approach gets extended to michael's accounts, and the principle
becomes foundational to the household's multi-machine setup.

## Decisions

| #  | Decision                                                                                 | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|----|------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | Recover/reconcile Wendy's UID across all 3 relevant machines before creating the account | Check `Backups-TM-Wendy-Pro` and wendy-owned files under `Backups-TM-Michael-Pro` (both dead, via NAS backups); ALSO check wendy's live UID on `wolf-air` directly (`dscl . -read /Users/wendy UniqueID`) since it's still running and, per user, may already disagree with the michael-pro/wendy-pro value. Use `stat`/`ls -ln` for the dead-machine backups. User will do this personally. If wolf-air's UID conflicts with the michael-pro/wendy-pro value, that conflict itself needs a decision before michael-air's `~wendy` UID is picked. |
| 2  | Account privilege: **admin**                                                             | Matches existing household convention -- Wendy is admin on all machines.                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 3  | Apple ID: her own, signed in locally in `~wendy`                                         | Not Michael's ID, not deferred -- this is what makes Safari/iCloud Drive genuinely hers.                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 4  | FileVault: add wendy to the unlock list                                                  | Confirmed FileVault is On (`fdesetup status`). Without this she can't unlock at cold boot/restart (Fast User Switch itself is unaffected).                                                                                                                                                                                                                                                                                                                                                                                                        |
| 5  | Touch ID: enroll her fingerprint on michael-air                                          | Per-machine (Secure Enclave, doesn't sync) + per-account (only unlocks her session). **wolf-air has no Touch ID hardware at all** -- password-only there regardless.                                                                                                                                                                                                                                                                                                                                                                              |
| 6  | Background RAM contention: no formal rule                                                | Her documented workload (50+ Safari tabs, RAM-bottlenecked) competing with your own use on a shared 16GB machine -- handled socially for now, revisit only if it's actually a problem.                                                                                                                                                                                                                                                                                                                                                            |
| 7  | Safari: full iCloud sync (tabs, bookmarks, history, Keychain/passwords)                  | This is what delivers "pick up where I left off on any machine."                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 8  | `~wendy/Documents`: trust iCloud Drive's own redundancy, don't force full local copies   | `~/Documents` is already TM-included ("valuable, irreplaceable") and that carries over automatically; accepted caveat that iCloud's "Optimize Mac Storage" may leave only local stubs (michael-air already near 90% disk use), making iCloud -- not the NAS TM backup -- the real durability backstop for her synced files.                                                                                                                                                                                                                       |
| 9  | TM backup scope: machine-level, not user-level (confirmed)                               | `tmutil`/TM prefs have no user-account exclusion mechanism -- only path- and volume-based. `tm-michael-air`'s existing whole-disk backup will include `/Users/wendy` automatically the moment the account exists; no new NAS account/share needed.                                                                                                                                                                                                                                                                                                |
| 10 | Reboot/update coordination: handle socially                                              | Give her a heads-up before restarting michael-air if her session is active; no technical guardrail (e.g., no forced-update lockout) for now.                                                                                                                                                                                                                                                                                                                                                                                                      |
| 11 | Document the login in `CONTEXT.md`                                                       | Still the right home for this fact -- nothing in the repo has superseded hand-maintained markdown registries; no tooling parses `CONTEXT.md` today so structured data wouldn't currently earn its keep.                                                                                                                                                                                                                                                                                                                                           |

## Manual Execution Guide (step-by-step, for you to run -- not automated)

Per your note: the TM network-share mounts below need to happen interactively (Finder
"Connect to Server" + Keychain/1Password credential prompt) -- auto-mounting a cold,
non-primary backup share is not reliable to script, so every command below assumes you're
sitting at the machine typing it, not running it unattended.

### Step 1 -- Recover/reconcile Wendy's UID across all 3 machines

**1a. Live check on wolf-air** (do this at wolf-air itself, or `ssh` in if remote access works):

```bash
dscl . -read /Users/wendy UniqueID
```

Record the number.

**1b. wendy-pro's historical UID, from the NAS backup:**

1. In Finder: **Go → Connect to Server** (`⌘K`)
2. Enter: `smb://192.168.8.129/Backups-TM-Wendy-Pro`
3. When prompted for credentials -- **note:** I could not find a documented service-account
   name for this specific share in the repo (michael-pro/michael-air have `tm-michael-pro`/
   `tm-michael-air` credentials in 1Password under "NAS - TM - tm-*"; no equivalent
   "NAS - TM - tm-wendy-pro" entry turned up in a repo search). Check 1Password's
   "Shared-Wolf Den" vault for whatever credential you actually used when this backup was
   set up -- it may or may not follow the `tm-wendy-pro` naming convention.
4. Once mounted, it should appear under `/Volumes/Backups-TM-Wendy-Pro`. Open it in Finder
   and look for a sparse bundle or a `Backups.backupdb`-style folder; open into the most
   recent dated backup snapshot down to the `Users/wendy` (or `Data/Users/wendy`, depending
   on the macOS version that created the backup) folder.
5. In Terminal, once you can see the mounted path, run (adjust the path to match what you
   actually find in step 4):

```bash
stat -f "%u %N" "/Volumes/Backups-TM-Wendy-Pro/<snapshot-date>/Data/Users/wendy/Documents"
```

   This prints the numeric UID that owns that directory. Record it.

**1c. michael-pro's record of wendy's UID (cross-check), same pattern:**

1. **Go → Connect to Server**: `smb://tm-michael-pro@192.168.8.129/Backups-TM-Michael-Air`
   -- wait, michael-pro's own backup share may be named differently; check
   `project-michael-air/TM-SETUP-PLAN.md` / `PLAN-names-networks-backups.md` for the exact
   share name if `Backups-TM-Michael-Pro` doesn't mount directly. Credential is
   `tm-michael-pro` (confirmed in 1Password as "NAS - TM - tm-michael-pro").
2. Navigate to a snapshot, look for any wendy-owned path (e.g. a shared/cross-mounted
   folder, if one ever existed) and `stat -f "%u %N"` it the same way as 1b.
3. Compare the three numbers (wolf-air live, wendy-pro backup, michael-pro backup). If they
   don't all agree, decide which one wins before step 4 below -- recommend: whichever value
   wolf-air currently has live, since that's the one account still actually in daily use.

### Step 2 -- Determine if wendy-pro had `~wendy/Documents` iCloud-enrolled

While still browsing the mounted wendy-pro backup snapshot from step 1b:

```bash
ls -la "/Volumes/Backups-TM-Wendy-Pro/<snapshot-date>/Data/Users/wendy/" | grep -i documents
```

- If `Documents` is a **symlink** pointing into
  `Library/Mobile Documents/com~apple~CloudDocs/Documents`, it was already iCloud-enrolled
  -- step 8 below will be a no-op re-download once she signs into iCloud on michael-air.
- If `Documents` is a **plain directory**, it was never enrolled -- you'll need the
  conditional restore described in step 8.

If you want to grab the actual file content now (in case you don't want to keep this share
mounted through every later step), copy it locally while you're here:

```bash
mkdir -p ~/Desktop/wendy-pro-documents-recovered
cp -R "/Volumes/Backups-TM-Wendy-Pro/<snapshot-date>/Data/Users/wendy/Documents" ~/Desktop/wendy-pro-documents-recovered/
```

### Step 3 -- Create the `~wendy` account on michael-air

System Settings → Users & Groups → **Add Account…** → Administrator → name "Wendy" /
account name `wendy`. macOS's GUI account creation does **not** let you set a specific UID
-- it auto-assigns the next available one (typically 502+). To force the UID you recovered
in step 1, create the account via `sysadminctl` in Terminal instead (requires the number
from step 1c's decision):

```bash
sudo sysadminctl -addUser wendy -fullName "Wendy" -password - -UID <recovered_uid> -admin
```

(`-password -` prompts interactively rather than putting her password on the command line
or in shell history.) Verify:

```bash
dscl . -read /Users/wendy UniqueID
```

### Step 4 -- FileVault unlock list

```bash
sudo fdesetup add -usertoadd wendy
```

You'll be prompted for wendy's password and an existing FileVault-enabled admin's
credentials (yours). Verify:

```bash
fdesetup list
```

### Step 5 -- Sign into Wendy's Apple ID

Fast User Switch into `~wendy` (menu bar → your name → Wendy, or `⌃⌘Q` then switch), then:
System Settings → sign in with **her** Apple ID (not yours). This has to be done logged in
as her -- there's no CLI for this step.

### Step 6 -- Safari + iCloud Keychain sync

Still inside `~wendy`: System Settings → [her name] → iCloud → toggle on **Safari** and
**Passwords & Keychain**.

### Step 7 -- iCloud Drive

Same iCloud settings pane → toggle on **iCloud Drive** → enable **Desktop & Documents
Folders**. Wait for the initial sync/merge dialog if macOS detects an existing local
`~wendy/Documents` (it will offer to merge local content into iCloud Drive -- this is where
the restored files from Step 2 get uploaded if Documents wasn't already enrolled on
wendy-pro).

If you saved a local copy in Step 2, copy it in now (after Desktop & Documents Folders is
already on, so it uploads rather than sitting local-only):

```bash
cp -R ~/Desktop/wendy-pro-documents-recovered/Documents/* ~/Documents/
```

(run this as `~wendy`, not as yourself -- paths above assume you're logged in as her when
you run it).

### Step 8 -- Touch ID

Still as `~wendy`: System Settings → Touch ID & Password → Add a Fingerprint. Physical
step, no command line.

### Step 9 -- Verify TM coverage

Switch back to `~michael`:

```bash
tmutil isexcluded /Users/wendy
```

Should print `[Included]`. After the next scheduled backup completes, confirm:

```bash
tmutil listbackups
```

and browse one to confirm `Users/wendy` is present.

### Step 10 -- Update CONTEXT.md

```bash
cd ~/repos/wolf-soho
$EDITOR CONTEXT.md
```

Add under the michael-air entry: `Additional login: wendy (admin, interim access pending wendy-air)`.

```bash
git add CONTEXT.md
git commit -m "Note wendy's interim login on michael-air"
```

### Step 11 -- Log the naming-strategy TODO

Add to `Identity Strategy - NAS + MB - Human+Service Accounts.md` (or this
`plan-shared-logins.md`): "TODO: Evaluate whether to make machine names independent of user
names -- to make clear what config is machine-specific and what is user-specific." Commit
with a clear message.

## Deferred / Out of scope for this plan

- Extending unified-login architecture to `michael` having consistent logins on all 3
  machines -- only after this wendy proof-of-concept proves stable.
- Retiring `wolf-air` -- trigger condition is wendy-air's purchase/setup, not this plan.
- Renaming machines to be person-independent -- logged as a TODO, not actioned now.
- Any technical guardrail against surprise reboots (e.g. disabling unattended updates) --
  handled socially per Decision 10.

## Verification

- `dscl . -read /Users/wendy UniqueID` on michael-air matches the UID recovered from the
  NAS backups.
- `fdesetup list` shows wendy as FileVault-enabled.
- Fast User Switch to wendy, confirm Touch ID unlocks her session.
- On wendy's iPhone or another Apple device, confirm the expected "new sign-in" security
  alert appeared (expected, not a problem).
- After the next scheduled TM run, confirm `/Users/wendy` appears in the backup (browse
  the backup or check `tmutil listbackups` contents) without any NAS-side reconfiguration.
- `CONTEXT.md` diff shows the new login line under michael-air.
