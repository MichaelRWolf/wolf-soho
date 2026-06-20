# AT&T Loging Fuckery

## Exodus from att.net and Mail.app

### Email Service Alternatives (You Pay, You're the Customer)

**Paid Email Services:**

- **Fastmail** - $3-5/month, excellent IMAP support, no ads, privacy-focused
- **ProtonMail** - $4-8/month, end-to-end encryption, Swiss-based privacy
- **Zoho Mail** - $1-4/month, business-focused, good IMAP/SMTP support
- **Tutanota** - €1-6/month, German-based, encrypted email
- **Posteo** - €1/month, German-based, eco-friendly, privacy-focused
- **Mailbox.org** - €1-3/month, German-based, GDPR compliant
- **Runbox** - $2-7/month, Norwegian-based, privacy-focused

**IMAP Mail Services (Custom Domain Support):**

- **Fastmail** - Full IMAP/SMTP, custom domains, excellent reliability
- **Zoho Mail** - Business IMAP, custom domains, good uptime
- **Google Workspace** - $6/month, Gmail with custom domain (you pay, not the product)
- **Microsoft 365** - $6/month, Outlook with custom domain
- **Rackspace Email** - $2/month, pure email hosting, no other services

### Email Client Alternatives (Modern Authentication Support)

**Cross-Platform:**

- **Spark** - Excellent OAuth 2.0 support, modern UI, free/paid tiers
- **Airmail** - Highly customizable, OAuth 2.0 support, $5
- **Thunderbird** - Mozilla's client, actively maintained, free
- **Outlook** - Microsoft's client, excellent OAuth 2.0 support, free

**macOS Specific:**

- **Canary Mail** - Modern, OAuth 2.0 support, $20/year
- **Mimestream** - Native macOS, Gmail-focused, $50/year
- **Postbox** - Thunderbird-based, enhanced features, $40

**Criteria for Selection:**

- You pay them money (you're the customer)
- They provide technical service (not selling your data)
- Modern authentication support (OAuth 2.0)
- No ads, no data mining
- Reliable uptime and support
- Can import historical data from @att.net IMAP

## 2026-06-20 -- Safari works, Chrome fails at OTP (errorCode=908)

### Observation

- **Safari**: full browser login succeeds -- email → password → SMS OTP (6-digit code to ...7941) → inbox
- **Chrome**: login proceeds to OTP page; correct code entered; page reloads with `errorCode=908`
  in URL; OTP not accepted; cannot proceed to inbox
- Error URL fragment: `signin.att.com/...IAM_OP=OTP&...&errorCode=908`
- After failure: OTP field resets to empty; "Be sure to enter a 6-digit verification code" shown --
  this is the post-rejection reset state, not a pre-submission validation warning

### Critical baseline: this is a server-side rejection

`errorCode=908` appears in ATT's redirect URL back to the OTP page. This means:

- Chrome **did** submit the OTP form (no client-side form failure)
- ATT's server **received** the submitted code
- ATT's server could **not validate** it and redirected back with errorCode=908
- The OTP field resets empty -- this is the post-rejection state, not a pre-submission warning

Any hypothesis must explain why ATT's server rejects a correct code submitted from Chrome
but not from Safari. Client-side form problems are eliminated.

### Hypothesis audit

#### H1 -- Chrome storage partitioning (CHIPS) breaks session continuity

ATT's login flow crosses multiple top-level sites (the redirect chain goes:
att.com → signin.att.com → oidc.idp.clogin.att.com → att-yahoo.att.net → yahoo.com).
Chrome's CHIPS (Cookies Having Independent Partitioned State) isolates cookies by top-level
site context. If the session cookie used to identify the OTP challenge was set in one
top-level context and the OTP submission happens in another, Chrome presents a different
cookie jar and ATT cannot find the session.

|                  |                                                                                                                      |
|------------------|----------------------------------------------------------------------------------------------------------------------|
| Evidence FOR     | Chrome has CHIPS; Safari does not; the ATT flow spans multiple domains                                               |
| Evidence AGAINST | The OTP form action appears to be on signin.att.com; if both pages are same-origin the partitioning should not apply |
| Weakness         | Cannot confirm or deny without reading Chrome DevTools Network/Cookie tabs during the flow                           |
| Confirms if      | Allowing all cookies in Chrome → OTP succeeds                                                                        |
| Invalidates if   | Allowing all cookies in Chrome → OTP still fails                                                                     |

---

#### H2 -- OTP code already consumed by Safari session

User tried Safari first (it worked). ATT then sent the Chrome session's OTP challenge. If ATT
rate-limits OTP issuance per phone number (won't send a fresh code while one is still active),
the Chrome session may be trying to validate an OTP that the Safari session already consumed or
that was issued to a different session. errorCode=908 = "session not found or code already used."

|                  |                                                                                                                                                                   |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Evidence FOR     | Safari succeeded first; Chrome immediately followed; SMS OTPs are often one-time-use                                                                              |
| Evidence AGAINST | Chrome showed the "We sent a verification code" page, implying it received its own challenge; user says "same thing on Chrome" suggesting a full independent flow |
| Weakness         | Unknown whether ATT sends a new code per session or rate-limits per phone number                                                                                  |
| Confirms if      | Waiting 10+ minutes after Safari success then repeating full Chrome flow → OTP succeeds                                                                           |
| Invalidates if   | Chrome still fails with a fresh session started long after Safari                                                                                                 |

Highest-priority alternative to test -- requires no Chrome changes, just timing.

---

#### H3 -- Chrome extension interferes with OTP submission

A Chrome extension (1Password, ad blocker, tracker blocker) could modify the OTP form POST:
add/remove headers, alter field values, or intercept the request.

|                  |                                                                                                                                                     |
|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| Evidence FOR     | Chrome was the failing browser; extensions run in Chrome only                                                                                       |
| Evidence AGAINST | errorCode=908 implies ATT received something; extension interference would more likely cause a network error or client-side form validation failure |
| Confirms if      | Chrome incognito (extensions disabled) → OTP succeeds                                                                                               |
| Invalidates if   | Chrome incognito → OTP still fails                                                                                                                  |

Easiest test to run -- incognito takes 30 seconds.

---

#### H4 -- SameSite=Strict or Lax cookie attribute blocking

ATT sets the session cookie without a modern SameSite attribute (or with Strict). Chrome defaults
missing SameSite cookies to Lax. If any part of the OTP submission is classified as a cross-site
POST (e.g., form action on a different subdomain than the page), Chrome drops the cookie.
Safari did not enforce SameSite=Lax as aggressively during its rollout.

|                  |                                                                                                                                       |
|------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| Evidence FOR     | Chrome enforces SameSite since Chrome 80 (2020); the ATT flow uses multiple subdomains                                                |
| Evidence AGAINST | If the OTP form POSTs to signin.att.com and the session cookie is on signin.att.com, it is same-site; SameSite=Lax would not block it |
| Overlap with H1  | Both are cookie-blocking mechanisms; H1 (CHIPS) is the more modern and more likely Chrome-specific variant                            |
| Confirms if      | Same test as H1: allow all cookies in Chrome                                                                                          |
| Invalidates if   | Same test as H1: allow all cookies and OTP still fails                                                                                |

---

#### H5 -- ATT behavior differs by User-Agent / browser fingerprint

ATT's server treats Chrome's User-Agent differently, applying stricter security checks that
produce errorCode=908 even for a correct code.

|                  |                                                                                |
|------------------|--------------------------------------------------------------------------------|
| Evidence FOR     | ATT's platform is old and has known browser-specific bugs                      |
| Evidence AGAINST | Chrome is the world's most common browser; explicit rejection is very unlikely |
| Low probability  | Would be an unusual and specific ATT decision                                  |
| Confirms if      | Spoofing Safari UA in Chrome → OTP succeeds                                    |
| Invalidates if   | UA spoofing has no effect                                                      |

---

### Ranked likelihood

1. **H2 (OTP already consumed)** -- highest priority to test; explains everything without needing Chrome-specific behavior; requires only timing
2. **H1/H4 (Chrome cookie partitioning/SameSite)** -- mechanically plausible; consistent with Chrome's known security trajectory; one test covers both
3. **H3 (Chrome extension)** -- easiest to test (incognito); low prior probability
4. **H5 (User-Agent fingerprinting)** -- low probability; test only if others ruled out

---

### Diagnostic tests (in order of priority)

#### Test A -- Timing (targets H2)

Wait at least 15 minutes after the Safari success. Start a completely fresh Chrome session.
Complete the full login flow. Enter the fresh OTP code within 30 seconds of receiving it.

- Passes → H2 confirmed (prior OTP consumed; fresh session works)
- Fails → H2 eliminated; proceed to Test B

#### Test B -- Chrome incognito (targets H3)

```bash
open -a "Google Chrome" --args --incognito "https://mail.yahoo.com/"
```

Complete the full flow. No extensions active in incognito.

- Passes → H3 confirmed (extension interference)
- Fails → H3 eliminated; extensions are not the cause

#### Test C -- Allow all cookies in Chrome (targets H1/H4)

Chrome → Settings → Privacy and security → Third-party cookies → Allow all.
Retry full login flow. Restore setting afterward.

- Passes → H1 or H4 confirmed (Chrome cookie policy blocking ATT session)
- Fails → H1 and H4 eliminated; look to H2 or H5

#### Test D -- DevTools inspection (definitive for H1/H4)

During the Chrome login flow: DevTools → Application → Cookies → signin.att.com.
Note which cookies are set after password entry. Confirm they are still present when
the OTP page loads and when the OTP form is submitted (check Network tab for POST headers).
Console may show "SameSite" warnings if cookie blocking is occurring.

#### Test E -- User-Agent spoof (targets H5, last resort)

In Chrome DevTools → Network conditions → set UA to Safari/WebKit UA string. Retry login.

- Passes → H5 confirmed
- Fails → H5 eliminated

---

### Consistency with prior documented failures

| Prior diagnosis                                           | Consistent?           | Notes                                                                           |
|-----------------------------------------------------------|-----------------------|---------------------------------------------------------------------------------|
| "It's not you, it's us" -- ATT ↔ Yahoo federation failure | Separate failure mode | Prior failure = post-auth handoff; 2026-06-20 failure = mid-auth OTP validation |
| Session corruption / identity collision                   | Not applicable        | Reaching OTP means ATT resolved the identity and sent an SMS                    |
| Account resolution failure                                | Not applicable        | OTP delivery is proof the account was resolved                                  |
| Chrome password manager saves wrong credential            | Not applicable        | OTP page has no saved credential; Chrome PM is irrelevant at this step          |

**New distinct failure mode**: server-side OTP validation failure (errorCode=908) in Chrome only.

### Implication for HOWTO

`HOWTO_att_yahoo_login_v2.md` updated 2026-06-20 to recommend Safari as Workflow A.
Chrome is now a known-broken fallback with diagnostic steps.

### Context

Discovered during wolf-air mail setup after michael-pro water damage (2026-06-18).
See [2026-06-18_michael-pro_water-damage.md](../2026-06-18_michael-pro_water-damage.md).

---

## 2025-08-14

### Summary of Attempts and Blockages

**What We Tried:**

- Attempted login to `https://signin.att.com` via multiple browsers (Chrome, Safari, incognito modes)
- Tried `https://currently.att.yahoo.com` and `https://mail.yahoo.com` redirects
- Investigated iOS Mail app authentication method (found it uses legacy SMTP with Secure Mail Key)
- Discovered AT&T's M&A clusterfuck with account linking between wireless and email services

**Where We Got Blocked:**

- All web portals return "It's not you, it's us" error page - AT&T's authentication system is completely down
- Care Code 201 [LU100] errors on all login attempts (indicates authentication failure/account security lock)
- Cannot access Secure Mail Key management without web portal access
- iPhone Mail app works (using existing SMK) but MacBook Mail.app needs its own SMK

**Key Findings:**

- iPhone uses legacy authentication (smtp.mail.att.net, port 465, SSL) with Secure Mail Key
- AT&T requires separate SMKs for each device/app that doesn't support OAuth 2.0
- Account name "Y! - MRW w/SMK" confirms previous SMK setup was successful
- AT&T's web authentication portal is completely broken (server-side issue)

### Next Steps

**First Step - Verify Portal Status:**
Before attempting any login procedures, verify that AT&T's web portal is functional:

1. Try accessing `https://signin.att.com` in a fresh browser session
2. If still showing "It's not you, it's us" error, wait and retry later
3. Only proceed with login attempts when portal returns normal login page

**When Portal is Working:**

1. Attempt login via `https://signin.att.com` (bypass myAT&T Profile if possible)
2. Navigate to Secure Mail Key management
3. Generate new SMK specifically for MacBook Mail.app
4. Update Mail.app preferences with new SMK

**Alternative Approaches:**

- Try accessing email account management through wireless myAT&T Profile if email is "linked"
- Contact AT&T support specifically about "legacy email account linking" issues
- Consider switching to third-party email client with OAuth 2.0 support

## 2025-08-13

### Problem

My  iphone can get mail from att.net. The password has not changed. Yet webmail on att.net and mail.app on macbook are refusing to sign in. More at&t fuckery. I really do not want to start a 1 hour password change/rechange/rechange/rechange redistribute-to-all-devices in a timing race condition fuckery. What's a good way to use iphone to convince macbook and chrome that I really do know my password and that at&t is fucked again. How to unfuck them? ChatGPT said: Regeneration must have conversation_id Retry No file chosenNo file chosen ChatGPT can make mistakes. Check important info. ChatGPT says:

### ChatGPT Suggestions

Got it -- you want a way to **leverage the fact that your iPhone is already logged in** to bypass AT\&T's broken sign-in process on your MacBook and Chrome, without triggering their "reset password" circus.

Here's the practical, minimal-frustration approach:

---

### 1. **Check if your iPhone can give you a "real" session cookie or token**

If your iPhone Mail app is still pulling messages, then AT\&T's IMAP/SMTP authentication is fine -- it's just the *webmail* (via browser) and Mac Mail that are choking.

- On your iPhone, go to **Safari** and try to log in to [currently.att.yahoo.com](https://currently.att.yahoo.com) or [mail.yahoo.com](https://mail.yahoo.com).

  - If it works there, you now have an active browser session on your iPhone.
  - You can use **iCloud Keychain** to sync that saved password across devices -- no retyping or re-entering required.
  - Sometimes, logging in via Yahoo's portal instead of AT\&T's triggers a working session that Mac Mail can then accept.

---

### 2. **Try "app-specific password" for the MacBook**

AT\&T/Yahoo sometimes blocks logins if they detect "older" mail clients. You can:

- In AT\&T/Yahoo account security settings (on iPhone Safari), create an **app password**.
- Use that app password in Mac Mail instead of your normal one.
  (This avoids AT\&T thinking the Mac is "suspicious.")

---

### 3. **Token-sharing workaround (cookies export)**

If you can get AT\&T Webmail working in Safari on your iPhone:

- Use a browser extension on Mac (like *EditThisCookie* in Chrome) to **import cookies** from the iPhone session.

  - You can export them on iPhone via **Safari Developer > Remote Automation** (requires enabling Web Inspector in iOS settings and connecting via USB to your Mac).
  - This gives Chrome the *exact same logged-in session*, skipping the password prompt.

---

### 4. **Use iCloud Keychain password sync**

If your iPhone already has the correct password saved in Safari/Keychain:

- Go to **System Settings > Apple ID > iCloud > Passwords & Keychain** on both devices -- turn it on.
- Once synced, just choose the autofilled password on Mac Mail/Chrome instead of typing it.
- This prevents typos or "wrong password" rejections caused by AT\&T's janky login parser.

---

### 5. **Bypass AT\&T's own portal**

Sometimes AT\&T's own login page is down while Yahoo's backend is fine.

- Go straight to: [https://mail.yahoo.com](https://mail.yahoo.com)
  and use your full att.net email as username.
- If you can log in there on Mac, it will often start working in Mac Mail without changing passwords.

---

If you want, I can give you a **step-by-step for the "cookie transplant" trick** so your Chrome and Mac Mail think you're already logged in like your iPhone is -- no password re-entry at all.

Do you want me to write that out? That's the most bulletproof way to avoid AT\&T's "password change" trap.
