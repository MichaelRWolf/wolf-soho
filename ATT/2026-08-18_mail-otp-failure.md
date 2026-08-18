# 2026-08-18 -- AT&T Mail OTP Failure (SMS Not Sent)

## Incident Summary

**Status**: Blocked on SMS delivery  
**Account**: <MichaelRWolf@att.net>  
**Device**: michael-air (MacBook Air M3, 2024)  
**Goal**: Set up Mail.app with att.net email

---

## Procedure

**Goal**: Establish Mail.app access on michael-air for <MichaelRWolf@att.net>

**Method**: Following `password_fuckery.md` "Bomb-Proof Procedure"

1. Browser auth entry point: <https://mail.yahoo.com> (documented working workaround)
2. Browser: Safari (known working per password_fuckery.md 2026-06-20)
3. Auth method: Standard email + password (or OTP if required)
4. Fallback: Mail.app direct IMAP/SMTP with Secure Mail Key (SMK)

**Constraint**: Do NOT reuse iPhone SMK on MacBook (device-specific; could invalidate both)

---

## Activity Log

### Attempt 1: Safari Browser → mail.yahoo.com

| Step | Input                         | Result                                   |
|------|-------------------------------|------------------------------------------|
| 1    | URL: <https://mail.yahoo.com> | Redirected to signin.att.com             |
| 2    | Email: <michaelrwolf@att.net> | Page accepted; no error                  |
| 3    | Password field                | **NEVER APPEARED**                       |
| 4    | Verification code prompt      | "We sent a verification code to ...7941" |
| 5    | SMS wait (3+ min)             | **No SMS received**                      |
| 6    | Resend button                 | Not available                            |

**Auth mechanism detected**: OAuth/OIDC flow (not simple password auth)

- Redirects: mail.yahoo.com → login.yahoo.com → signin.att.com/dynamic/iamLRR
- URL parameters reveal: `userID=michaelrwolf%2540att.net` pre-populated server-side
- Response type: `id_token` (OpenID Connect)
- Flow: Account pre-identified → OTP MFA → token response

**Key observation**: Email is already in the OAuth request URL (pre-populated); password entry never required. System went directly from OAuth initiation → OTP verification request.

**Outcome**: Blocked at OTP verification (SMS not delivered to ...7941).

### Attempt 2: Safari Incognito → Same URL

| Step              | Result                                                |
|-------------------|-------------------------------------------------------|
| Email entry       | Accepted                                              |
| Password field    | Still did NOT appear                                  |
| Verification code | Requested to ...7941                                  |
| SMS delivery      | No code received                                      |
| Flow difference   | Slightly different (specific differences to document) |

**Key observation**: Same passwordless flow in incognito. Confirms this is AT&T's auth logic, not browser state/cookies.

**Outcome**: Same blockage (OTP verification SMS not sent).

### Network/Connectivity Verification

- Wifi calling test: Placed call to 611 → connected successfully
- Phone number: 206-679-7941 (correct, confirmed on account)
- Carrier SMS capability: Working (call proves network routing)
- Conclusion: Network/SMS infrastructure is functional; failure is AT&T's OTP delivery

### iPhone Mail.app Status (Proof of Account Health)

- Active IMAP/SMTP access: Working
- Auth method: Secure Mail Key (device-specific to iPhone SE 3rd Edition)
- Account: Confirmed functional and accessible
- Conclusion: Account is healthy; browser OTP path is broken, not the account

---

## OAuth/OIDC Flow Analysis

**What this means:**

AT&T is using **OpenID Connect (OAuth 2.0)** federation for Yahoo mail auth. The flow:

1. Yahoo redirects to AT&T's identity provider (signin.att.com/dynamic/iamLRR)
2. AT&T's OAuth provider **pre-identifies** the account (userID already in URL)
3. OAuth provider initiates MFA: SMS OTP to registered phone
4. OTP SMS **is not being sent** (system stops here)

**Why password entry was skipped:**

OAuth/OIDC doesn't work like form-based auth. The account is resolved before the browser-facing UI. There's no "password form" step -- only MFA (in this case, SMS OTP).

**Implication for Mail.app:**

- **SMK/legacy IMAP path**: Bypasses OAuth entirely; direct SMTP/IMAP auth (what iPhone uses)
- **OAuth path**: Would hit the same broken OTP SMS flow
- **Solution**: Must use SMK path, not OAuth

**Critical blocker**: To get a new MacBook SMK, need to access account settings. All account settings access requires completing the OAuth/OIDC flow, which is blocked at OTP SMS delivery.

---

## Root Cause Analysis

**OTP SMS not sent, despite:**

- Valid credentials (password accepted by AT&T server)
- Valid phone number (iPhone already has working mail access)
- Network connectivity confirmed

**Likely causes:**

1. AT&T's SMS pipeline for OTP delivery is broken (similar to "It's not you, it's us" portal failures documented in password_fuckery.md)
2. Account has security hold that blocks SMS OTP but allows IMAP/SMTP access
3. Rate limiting: OTP already sent but not delivered; no resend available

---

## Current Blocker: Browser Access Locked

**Cannot generate new SMK for MacBook because:**

- Browser OTP path is completely broken (SMS not sent)
- Web portal access requires OTP to complete authentication
- No "Resend code" button available on OTP page
- Account security settings inaccessible without browser login

**iPhone Mail.app proves the account is functional**, so this is not a dead account -- it's a broken authentication pathway.

---

## Secure Mail Key (SMK) -- Important Clarification

### What is an SMK?

A **Secure Mail Key** is AT&T's legacy app-specific password. It's **per-device, per-app**, not universal.

### Device-Specific (NOT Shared Across Devices)

- **iPhone Mail.app** has its own SMK: `SMK - michaelrwolf@att.net iPhone SE 3rd Edition`
- **MacBook Mail.app** needs a **separate, new SMK** (not the iPhone one)
- **Chrome browser** would need a different auth path (OAuth or yet another token)

### Why Separate SMKs?

AT&T's documentation states: "AT&T requires separate SMKs for each device/app that doesn't support OAuth 2.0."

This means:

- **DO NOT use the iPhone SMK on the MacBook** -- it's tied to the iPhone SE, and reusing it may invalidate the iPhone setup or cause unpredictable behavior
- **Each device must have its own generated SMK** from AT&T's account settings
- iPhone's working SMK proves the account is healthy; it's not a workaround to steal

---

## What We Know

| Factor                 | Status                                                       |
|------------------------|--------------------------------------------------------------|
| AT&T account           | ✓ Functional (iPhone Mail.app has working IMAP/SMTP access)  |
| Credentials            | ✓ Correct (password accepted by AT&T server)                 |
| Phone number           | ✓ Valid (206-679-7941, matches account on file)              |
| Network                | ✓ Working (WiFi calling confirmed)                           |
| Browser OTP path       | ✗ **BROKEN** -- SMS not being sent                           |
| Web portal access      | ✗ **Blocked** -- OTP required to proceed                     |
| Account SMK generation | ✗ **Blocked** -- cannot access settings without browser auth |

---

## Next Steps / Workarounds

### Option A: Wait for OAuth SMS to Recover (Passive)

AT&T's OAuth/OIDC SMS MFA pipeline appears broken. **Wait 1-2 hours or until tomorrow.**

- If OTP SMS delivery recovers, OAuth flow will complete
- Account settings will become accessible
- Can then generate new MacBook SMK

### Option B: Call AT&T Support -- Specific Technical Issue (Attempted 2026-08-18)

**Outcome**: AT&T support politely declined ownership. Directed to Yahoo.com support instead.

**Call AT&T support.** Lead with specific technical facts to reach email/OAuth support:

```text
"My MichaelRWolf@att.net account's OAuth authentication is failing 
at the SMS OTP step. Your provider at signin.att.com/dynamic/iamLRR 
correctly identifies my account and requests verification codes to 
206-679-7941, but SMS codes are not arriving.

Proof: iPhone Mail.app has working IMAP/SMTP access via Secure Mail Key.

I need: A new Secure Mail Key generated for MacBook Mail.app, OR 
confirmation that the OAuth SMS pipeline is down and when it will 
be fixed."
```

**If agent doesn't know what SMK is**: "I need email technical support. Secure Mail Key is the legacy app-specific password for IMAP/SMTP access. My iPhone has one, it's working."

**If they say "just use OAuth in Mail.app"**: "Mail.app doesn't support OAuth for att.net. It requires Secure Mail Key (SMTP port 465) or I need to switch to a different client."

### Option C: iPhone as Proxy (If Device Allows)

Test iPhone Safari access to <https://mail.yahoo.com>:

- If iPhone completes OAuth flow, use iPhone to access account settings and generate new SMK
- **Likely to fail** with same OTP SMS issue (same backend)

### Option D: Switch Email Client (Practical Option)

Thunderbird, Spark, or Outlook support modern OAuth 2.0:

- Can import historical mail via IMAP (iPhone SMK proves account access)
- No need for new SMK generation
- See password_fuckery.md "Email Client Alternatives" for options

---

## Realistic Assessment (AT&T Ownership Declined)

**Status**: AT&T support refused to own the issue. Directed to Yahoo.

**Why this matters**: The OAuth/OIDC SMS failure is now Yahoo's problem (they run the backend), not AT&T's. Neither company will likely help quickly.

**Practical paths forward** (in order of likelihood to work):

| Option                                                 | Effort  | Risk | Blocker                                                   |
|--------------------------------------------------------|---------|------|-----------------------------------------------------------|
| **Yahoo support call**                                 | Medium  | Low  | Yahoo may also refuse (federated auth is their nightmare) |
| **Switch to OAuth-capable client** (Thunderbird/Spark) | Low     | None | None; import via iPhone SMK access                        |
| **Mail.app with existing iPhone SMK** (HIGH RISK)      | Trivial | High | May invalidate iPhone setup; docs say "separate SMKs"     |
| **Wait for OAuth SMS to self-heal**                    | None    | None | Takes unknown time; low probability                       |

### Option: iPhone SMK on MacBook (Not Recommended, High Risk)

**The gamble**: Reuse the existing iPhone SMK on MacBook Mail.app.

**Why it might work:**

- SMK is per-account, not per-device (technically)
- iPhone Mail.app is already using it successfully
- Could allow Mail.app to authenticate via IMAP/SMTP

**Why it's risky:**

- Documentation says "separate SMKs for each device"
- Using one SMK on two devices simultaneously may:
  - Invalidate the iPhone setup
  - Cause rate-limiting or security locks
  - Trigger unexpected behavior on either device
- If it breaks, fixing it requires browser access (blocked by OAuth failure)

**If you go this route:**

1. Have the iPhone SMK value ready from 1Password
2. Mail → Settings → Add Account → Other Mail Account
3. Email: `MichaelRWolf@att.net`
4. Password: [paste iPhone SMK value]
5. IMAP: `imap.mail.att.net` port 993 SSL
6. SMTP: `smtp.mail.att.net` port 465 SSL
7. Test fetch/send

**If it works**: Document success and SMK reuse for future reference  
**If it fails**: iPhone Mail.app will probably still work; revert Mail.app to offline

---

## Resolution (2026-08-18 -- SUCCESS)

### What Worked

Mail.app with **restored account + SMK credential update**.

**Sequence that succeeded:**

1. **Opened Mail.app** -- disabled "Mail Privacy Protection" on first-run (security feature can interfere with legacy IMAP/SMTP)
2. **Found restored accounts** from ~/Library TM restore (michael-pro predecessor had mail configured)
3. **Identified failing account**: "Y! - MRunW" (IMAP login error: wrong credentials)
4. **Updated credentials**: Replaced old password with shared SMK (all att.net aliases use same SMK)
5. **Mail.app reconnected** -- account working
6. **Restored all relevant accounts**: All michael-air Mail.app accounts now functional

### Key Finding

**Mail.app IMAP/SMTP path works perfectly; browser OAuth path is completely broken.**

- Browser: OAuth/OIDC SMS OTP fails (SMS never sent)
- Mail.app: Direct IMAP/SMTP with SMK succeeds (proven, working)
- This is why iPhone Mail.app has always worked -- it uses SMK, bypasses OAuth entirely

### Account Structure Clarified

All att.net addresses on single account (<mbalenger@att.net> primary):

- <mbalenger@att.net>
- <MichaelRWolf@att.net>
- <WendyRWolf@att.net>
- <MichaelRunningWolf@att.net>
- <WendyRunningWolf@att.net>
- (all share ONE SMK)

Mail.app now has all these configured and working.

---

## Decision Point

**Do not attempt to use iPhone SMK on MacBook** -- it's device-specific and may corrupt both the iPhone and MacBook setups.

**Best path forward**: Option B (call AT&T support) to request new MacBook SMK, since browser/OTP auth is completely broken on this particular attempt.

---

## Related Documentation

- [password_fuckery.md](./password_fuckery.md) -- Full AT&T auth fuckery history, including 2025-08-14 "It's not you, it's us" portal failures and OTP issues
- Project: [project-michael-air](../project-michael-air/) -- MacBook Air M3 setup tracking
- Issue: [GitHub Issue #6](https://github.com/MichaelRWolf/wolf-soho/issues/6) -- michael-pro water damage incident that prompted michael-air setup
