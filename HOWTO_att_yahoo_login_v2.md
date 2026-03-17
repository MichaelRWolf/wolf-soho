# ATT Yahoo Mail Login — Clean HOWTO

## Concept Overview

ATT email is a **federated login**:

- You start at a Yahoo-branded page
- You authenticate at **signin.att.com** (ATT identity provider)
- You land in **Yahoo Mail** (mail.yahoo.com)

The ugly URL is just OAuth/OIDC plumbing. Ignore it.

There are **two credential modes**:

1. **ATT password (normal)** → works in browsers
2. **Secure Mail Key (app password)** → required for Mail apps (iPhone/macOS Mail)

Goal: **one 1Password item + one Secure Mail Key** → works everywhere.

---

## Tools

- 1Password (single source of truth)
- Browser (Chrome on macOS)
- iPhone Mail app
- macOS Mail app (optional)

---

## Workflow A — Browser (Chrome on macOS)

1. Go to:
   <https://currently.att.yahoo.com/>

```bash
open "https://currently.att.yahoo.com/"
```

1. Click **Mail**
2. You will be redirected to:
   <https://signin.att.com/>... (this is correct)

```bash
open "https://signin.att.com/"
```

### What is presenting the login?

- The **page = ATT**
- Chrome only offers to fill/save passwords

### Login

- Username: your ATT email
- Password: your **ATT password** (NOT Secure Mail Key)

### 1Password setup

Create ONE item:

- Title: `ATT Yahoo Mail`
- Username: your email
- Password: ATT password
- URL: <https://signin.att.com>

Turn OFF Chrome password manager so it stays out of the way.

### Disable Chrome Password Manager (macOS)

1. Open Chrome
2. Settings → Autofill & Passwords → Password Manager
3. Turn OFF:
   - Offer to save passwords
   - Auto Sign-in
4. Go to: `chrome://password-manager/passwords`

```bash
# NOTE: chrome:// URLs require Chrome explicitly
open -a "Google Chrome" "chrome://password-manager/passwords"
```

1. Delete any entries for:
   - att.com
   - yahoo.com
   - att.yahoo.com

Result: Chrome stops presenting choices entirely. 1Password becomes the only key source.

### Avoid macOS Keychain storage

- Do NOT allow apps to “Save password to Keychain”
- In Mail setup, paste the **Secure Mail Key** manually
- Store all credentials only in 1Password

Result: No credentials live in Keychain or browser.

---

## Workflow B — iPhone Mail App

ATT/Yahoo **will NOT accept your normal password** here.

You must create a **Secure Mail Key**:

1. Go to ATT profile/security settings
2. Create “Secure Mail Key”
3. Copy it

### Configure iPhone

- Settings → Mail → Accounts → Add Account → Yahoo
- Enter:
  - Email: your ATT email
  - Password: **Secure Mail Key**

### 1Password

Add to same item:

- Section: “Secure Mail Key”
- Value: generated key

---

## Workflow C — macOS Mail App

Same as iPhone:

- Use Yahoo account type
- Use **Secure Mail Key** (not normal password)

---

## Mental Model (this is the part that removes frustration)

- Browser login = **interactive OAuth → uses real password**
- Mail apps = **IMAP/SMTP → requires app-specific key**

So:

- If you see a web page → use password
- If you see a mail client → use Secure Mail Key

---

## Common Failure Modes

### Browser says “Incorrect user ID or password”

→ Your real ATT password is wrong/outdated (Mail.app may still work via Secure Mail Key or cached token)

### “It’s not you, it’s us.” (ATT error page)

→ Backend glitch or bad session
→ Retry in fresh incognito or different entry path (see Reset Password below)

### Infinite redirects / weird URLs

→ Normal. That’s ATT ↔ Yahoo handshake

### Chrome asking to save password

→ Disable Chrome password manager
→ Use 1Password only

---

## Reset Password (ATT Access ID)

Use this when browser login fails but Mail.app still works.

### Clean path (preferred)

1. Open fresh incognito:

```bash
open -a "Google Chrome" --args --incognito "https://signin.att.com/"
```

1. Enter your ID (e.g., <michaelrwolf@att.net>)
2. Click **Forgot password**

If you hit “It’s not you, it’s us.”:

- Retry via myAT&T entry:

```bash
open "https://www.att.com/my/"
```

- Or try direct reset page:

```bash
open "https://www.att.com/acctmgmt/fpwd/"
```

### During reset, note signals

- SMS to 206-679-7941 → same wireless account linkage
- Email verification → which mailbox?
- Security questions → legacy account path

### After reset

- Verify browser login works at signin.att.com
- Update 1Password with the NEW password
- Do NOT change Mail.app yet (it will keep working)

---

## Reset “Other Thing” (Secure Mail Key)

Use this if Mail.app stops working or you want to standardize.

1. Go to ATT profile/security:

```bash
open "https://www.att.com/my/#/profile/security"
```

1. Find **Secure Mail Key**
2. **Delete existing key** (if unsure) and **Create new key**
3. Store it in 1Password (same item, separate field)

### Apply to clients

- iPhone Mail / macOS Mail → replace password with new Secure Mail Key
- Browser → continues to use normal ATT password (NOT the key)

### Sanity check

- Mail works with key
- Browser works with password

---

### “Password doesn’t work” in Mail app

→ You used your real password instead of Secure Mail Key

### Infinite redirects / weird URLs (Secure Mail Key)

→ Normal. That’s ATT ↔ Yahoo handshake

### Chrome asking to save password (Secure Mail Key)

→ Disable Chrome password manager
→ Use 1Password only

---

## Minimal Setup Checklist

- [ ] 1Password item created (ATT password)
- [ ] Secure Mail Key generated and stored
- [ ] Browser login works
- [ ] iPhone Mail works
- [ ] macOS Mail works

---

## Passkeys (what they are and how they fit)

Passkeys are **passwordless credentials** based on public/private key crypto:

- Stored in: 1Password, iCloud Keychain, or Google Password Manager
- You authenticate with: Face ID / Touch ID / device unlock
- The website never sees a password

### Key point

A passkey is tied to **where it is stored**:

- 1Password passkey → portable across devices
- Google passkey → tied to Chrome/Google account
- Apple passkey → tied to iCloud Keychain

👉 Your goal aligns with:
**Store passkeys ONLY in 1Password**

---

## Google Password Manager — what it is doing

Google Password Manager stores:

- Passwords
- Passkeys
- Auto sign-in state

### How to inspect what Google is managing

In Chrome:

1. Go to: `chrome://password-manager/passwords`

```bash
# NOTE: chrome:// URLs require Chrome explicitly
open -a "Google Chrome" "chrome://password-manager/passwords"
```

   → shows saved passwords
2. Go to: `chrome://password-manager/passkeys`

```bash
# NOTE: chrome:// URLs require Chrome explicitly
open -a "Google Chrome" "chrome://password-manager/passkeys"
```

   → shows saved passkeys (if any)

You can also visit:

- <https://passwords.google.com>

```bash
open "https://passwords.google.com"
```

This is the **ground truth list** of what Google controls.

---

## Log Entry — 2026-03-17

![Google Password Manager Empty State (small)](image)

OCR Extracted Text:

Welcome to your Password Manager

You haven’t saved any passwords in your Google Account yet. Add saved passwords from Android or Chrome to strengthen your password security.

Learn more

---

## Is it safe to “Delete all Google Password Manager data”?

Yes — **IF** you confirm BOTH:

- [ ] Every login exists in 1Password
- [ ] Any passkeys you care about are ALSO in 1Password

### Danger zone

If a passkey exists ONLY in Google:
→ deleting it can lock you out
→ recovery depends on the site (often painful)

---

## Clean Migration Strategy (recommended)

1. Inspect:
   - `chrome://password-manager/passwords`

```bash
# NOTE: chrome:// URLs require Chrome explicitly
open -a "Google Chrome" "chrome://password-manager/passwords"
```

- `chrome://password-manager/passkeys`

```bash
# NOTE: chrome:// URLs require Chrome explicitly
open -a "Google Chrome" "chrome://password-manager/passkeys"
```

1. For each item:
   - Ensure it exists in 1Password

2. For passkeys:
   - If site supports it, create a **new passkey in 1Password**
   - Then delete the Google-stored one

3. After verification:
   - Delete all Google Password Manager data

---

## Final Desired State

- 1Password → owns all passwords + passkeys
- Chrome → stores nothing
- Keychain → stores nothing (by choice)

You now have **one key ring, not three competing ones**.

---

## AT&T Account Inventory (OCR from Keychain Screenshots)

Extracted identities:

- <michaelrwolf@att.net>
- <MichaelRunningWolf@att.net>
- <mbalenger@att.net>
- <michaelrwolf@att.net.id>
- <wendyrwolf@att.net>
- <wendyrunningwolf@att.net>
- 206-679-7941
- wolf425351
- 7SkHBdbHFT3UpXX1 (likely autogenerated / token)

Named entries observed:

- MRW 2025-08-16
- MRunW
- WRW 2022-12-18
- WRunW
- mbalenger (att.net alias)

---

## How AT&T Identities Actually Work (this untangles the mess)

AT&T has ONE identity system with multiple identifiers:

### Primary Identity (ATT Access ID)

This is the real account:

- Usually an email (att.net / sbcglobal / bellsouth)
- Or sometimes a phone number

Everything else is just an alias or login handle pointing to that.

---

### Types of login identifiers you are seeing

#### 1. Email addresses (att.net)

- <michaelrwolf@att.net>
- <mbalenger@att.net>
- <wendyrwolf@att.net>

These can be:

- Primary IDs
- Linked sub-accounts
- Legacy identities from pre-merger eras

#### 2. Phone number login

- 206-679-7941

Modern AT&T prefers this for wireless accounts.
It often maps to the same underlying account as an email.

#### 3. Aliases / usernames

- wolf425351
- MRunW / WRW / etc

These are older-style usernames or labels, not always valid login IDs anymore.

#### 4. Garbage / tokens

- 7SkHBdbHFT3UpXX1

These are NOT real logins:

- session artifacts
- OAuth identifiers
- cached credentials

Safe to ignore/delete once verified.

---

## Relationship: att.com vs att.net

- **att.com** = account management (billing, wireless, identity)
- **att.net** = email namespace (hosted by Yahoo)

But:
👉 They authenticate through the SAME system (signin.att.com)

So:

- One ATT Access ID
- Multiple ways to type it

---

## Why you see so many choices

Because over 25+ years:

- ATT merged systems (SBC, BellSouth, Yahoo)
- Added phone-based login
- Added aliases
- Cached everything in Keychain

Result = archaeological dig site 🏺

---

## What you should do (clean strategy)

### Step 1 — Pick ONE canonical login

Choose ONE:

- <michaelrwolf@att.net> (recommended)
OR
- phone number (if ATT pushes it)

Everything else becomes secondary.

---

### Step 2 — Verify linkage (SAFE METHOD — do NOT break anything)

You are correct to be cautious. Do NOT assume they are unified.

#### A. Test each identity independently (incognito)

For EACH of these:

- <michaelrwolf@att.net>
- <mbalenger@att.net>
- phone (206-679-7941)

Do this:

1. Open fresh incognito window
2. Go to:
   <https://signin.att.com/>

```bash
open -a "Google Chrome" --args --incognito "https://signin.att.com/"
```

1. Log in with ONE identity

2. After login, check:
   - Profile name
   - Billing account
   - Wireless account
   - Email inbox access

👉 Write down what account you landed in

---

#### B. Detect SAME vs DIFFERENT accounts

If two logins land you in:

- Same billing account
- Same phone plan
- Same profile

👉 They are aliases of ONE account

If they land in:

- Different billing
- Different profile

👉 You have MULTIPLE real accounts (do NOT unify blindly)

---

#### C. Email test (critical)

For each identity:

1. Go to mail via:
   <https://currently.att.yahoo.com/>

```bash
open "https://currently.att.yahoo.com/"
```

1. Confirm:
   - Same inbox?
   - Or different mailboxes?

👉 Same inbox = aliases
👉 Different inbox = separate accounts

---

#### D. Only AFTER this — choose canonical

You only collapse to ONE identity if:

- [ ] Same billing account
- [ ] Same wireless account
- [ ] Same email inbox

If ANY of those differ:
👉 Keep multiple identities (document them, don’t merge them)

---

#### E. Safety net (before cleanup)

Before deleting anything:

- [ ] Verify login works for each identity
- [ ] Store each in 1Password temporarily
- [ ] Confirm Secure Mail Key works for each mailbox

Only then:
👉 prune duplicates

---

### Key Insight (this is the trap you’re avoiding)

AT&T sometimes:

- links identities loosely
- but NOT fully

So things can look unified…
…but still break if you remove the wrong credential

👉 Treat this like data migration, not cleanup

Prove equivalence BEFORE consolidation

---

### Step 3 — Clean 1Password

Keep:

- ONE login (username + password)
- ONE Secure Mail Key

Optional notes section:

- list legacy aliases (for recovery only)

Delete:

- duplicates
- tokens
- partial entries

---

### Step 4 — Clean Keychain (optional but recommended)

Search for:

- att
- yahoo

Delete anything not actively used.

(This removes the UI clutter you showed.)

---

### Step 5 — Accept Mail.app behavior

Mail.app stores:

- Secure Mail Key
- OAuth tokens

This is expected and OK.

👉 You will NOT be prompted every time
👉 This is NOT Keychain chaos, it is session caching

---

## Final Mental Model

You do NOT have 10 accounts.

You have:
👉 1 account
👉 6–10 historical identifiers
👉 20 years of residue

Your job is not to "manage them all"

Your job is to:
👉 pick one
👉 prove it works
👉 ignore the rest

---

## ATT ↔ Yahoo Email Failure (KNOWN ISSUE + FIX)

### Symptom you saw

- Login to att.com works ✅
- Redirect to mail (currently.att.yahoo.com) fails ❌
- Error: “It’s not you, it’s us.”

👉 This is NOT your password
👉 This is a broken **ATT ↔ Yahoo session handoff**

---

### What’s actually happening

Flow:

1. You authenticate with ATT (success)
2. ATT tries to pass a token to Yahoo
3. Yahoo rejects it or session breaks

Result:
👉 You are logged in… but can’t reach mail

---

### Fix (clean session reset — this usually works)

#### Step 1 — hard reset cookies (targeted)

In Chrome:

- Open DevTools → Application → Storage
- Clear data for:
  - att.com
  - yahoo.com
  - att.yahoo.com

OR faster:

```bash
open -a "Google Chrome" --args --incognito "https://mail.yahoo.com/"
```

---

#### Step 2 — enter from Yahoo side (NOT ATT side)

Go directly to:

```bash
open "https://mail.yahoo.com/"
```

Then:

- Enter: <michaelrwolf@att.net>
- Use NEW password

👉 This often succeeds when ATT entry fails

---

#### Step 3 — if still broken (common edge case)

Force relink:

1. Go to:

```bash
open "https://www.att.com/my/#/profile/security"
```

1. Look for:
   - “Linked accounts”
   - “Email accounts”
2. Confirm att.net email is present

If missing or odd:
👉 linkage is partially broken (common for old accounts)

---

### Nuclear workaround (always works)

Use Yahoo direct login flow:

```bash
open "https://login.yahoo.com/"
```

- Enter att.net email
- Complete login

👉 Yahoo handles ATT federation better than ATT does

---

### Why Mail.app still works

Mail.app uses:

- IMAP + Secure Mail Key
- NOT the web OAuth handshake

So it bypasses this entire mess.

---

### Mental model upgrade

You now have TWO working paths:

- ATT account login → works
- Mail app → works
- ATT → Yahoo redirect → flaky

👉 This is a **system integration bug**, not your setup

---

### When to worry

Only worry if:

- Yahoo direct login ALSO fails

Otherwise:
👉 you are fully functional

---

## ATT ↔ Yahoo Failure — V2 (Session Corruption Edition)

### What we discovered (new)

There are TWO distinct failure classes:

#### 1. Federation failure (older section)

- ATT login works
- Yahoo handoff fails

#### 2. **Session corruption (your current state)**

- ATT login appears to work
- ANY ATT page (profile, etc.) fails immediately
- Error: “It’s not you, it’s us.”

👉 This means:
**ATT cannot resolve your session to an account**

---

## Root Cause (most likely)

Given your identity inventory:

- <michaelrwolf@att.net>
- <mbalenger@att.net>
- phone login
- multiple legacy aliases

👉 You likely have:
**multiple ATT identities partially overlapping**

ATT authenticates one
ATT tries to load another
ATT fails to resolve

💥 Result: global failure across ATT pages

---

## Fix — Session Layer Reset (REQUIRED FIRST)

### Step 1 — Delete ALL site data (not optional)

```bash
open -a "Google Chrome" "chrome://settings/siteData"
```

Delete EVERYTHING for:

- att.com
- yahoo.com
- signin.att.com
- att.yahoo.com

---

### Step 2 — Kill browser completely

```bash
killall "Google Chrome"
```

Reopen Chrome

---

### Step 3 — Enter from Yahoo (clean path)

```bash
open -a "Google Chrome" --args --incognito "https://mail.yahoo.com/"
```

Login with:

- <michaelrwolf@att.net>
- ATT password

---

### Expected result

- Redirect to ATT → success
- Return to Yahoo → inbox loads

---

## If this STILL fails

You are in:

👉 **Identity collision / account resolution failure**

This is NOT fixable client-side

---

## What to say to ATT (precise language)

> “My AT&T Access ID authenticates, but any account-level page returns ‘It’s not you, it’s us.’ The session cannot resolve to a single account. I believe multiple identities are linked to this Access ID.”

Key words that matter:

- Access ID
- session cannot resolve
- multiple identities

---

## Ground Truth Check

If Mail.app works:

- Mailbox exists ✅
- Credentials valid ✅
- IMAP works ✅

Only broken piece:
👉 Web session + federation

---

## Final Mental Model (V2)

You do NOT have a login problem.

You have:

- a valid identity 🔑
- a valid mailbox 📬
- a broken session resolver 🧩

---

## Voodoo Fuckery — Not credentials, Account resolution failure

### What this means

This is the current diagnosis.

It is **not**:

- wrong password
- wrong username
- browser autofill confusion
- Secure Mail Key confusion

It **is most likely**:

- AT&T session corruption
- account resolution failure
- identity collision between old linked identifiers
- broken ATT ↔ Yahoo federation for web login

### Ground truth established so far

These facts are already proven:

- `michaelrwolf@att.net` is a valid ATT Access ID
- password reset succeeded
- SMS verification to `...7941` succeeded
- Mail.app still works for this mailbox
- browser login can succeed far enough to show account-related pages
- web flows then die with **“It’s not you, it’s us.”**
- Yahoo direct and ATT direct both eventually hit the same failure

### Working diagnosis

The most likely model is:

1. ATT authenticates identity A
2. ATT/Yahoo tries to resolve account/mailbox context B
3. backend cannot reconcile them
4. web session dies

In plain English:

👉 **The credentials are valid, but AT&T cannot consistently map them to one account context.**

---

### Stop point for today

Do **not** spend more time today on:

- trying more URLs
- trying more browsers
- trying old passwords
- editing 1Password entries again
- deleting Mail.app accounts

That would just feed the swamp.

---

### Next steps to pick up later

When ready to resume, do this in order:

#### 1. Full Chrome site-data purge

Open Chrome settings and remove **all** data for:

- `att.com`
- `signin.att.com`
- `yahoo.com`
- `att.yahoo.com`

If `chrome://settings/siteData` is awkward or missing from the UI, use the Privacy path in settings and search for **site data** or **third-party cookies / all site data**.

Command reminder:

```bash
open -a "Google Chrome" "chrome://settings/siteData"
```

#### 2. Quit Chrome fully

```bash
killall "Google Chrome"
```

#### 3. Retry only one clean web path

```bash
open -a "Google Chrome" --args --incognito "https://mail.yahoo.com/"
```

Use:

- user: `michaelrwolf@att.net`
- password: current ATT password

#### 4. If the same failure returns

Stop client-side work.

At that point the next action is:

- contact AT&T support
- describe it as **account resolution failure**, not bad password

Use this wording:

> My AT&T Access ID authenticates and password reset succeeds, but any account-level or Yahoo mail web flow eventually fails with “It’s not you, it’s us.” Mail.app still works. The session appears unable to resolve to a single account, and I believe multiple historical identities are linked.

Keywords that matter:

- AT&T Access ID
- session cannot resolve
- multiple historical identities
- Mail.app still works
- web mail fails

#### 5. Optional evidence to have on hand

- screenshot of successful password reset / verification flow
- screenshot of ATT account home page
- screenshot of “It’s not you, it’s us.”
- known identifiers:
  - `michaelrwolf@att.net`
  - `mbalenger@att.net`
  - `206-679-7941`
  - `wolf425351`

---

### Resume marker for future conversation

If later you say:

“What is next to unfuck AT&T?”

pick up here:

1. confirm whether full Chrome site-data purge was done
2. confirm whether clean Yahoo-entry retry was done after purge
3. if yes and still failing, move directly to ATT support wording and escalation

---

## TL;DR

- Current failure is **not credentials**
- Best current diagnosis is **account resolution failure**
- Stop for today
- Next resume point is: full site-data purge, one clean Yahoo retry, then ATT support escalation if unchanged
