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

### Hypothesis: Chrome loses session state during OTP step

ATT's login is a multi-hop OAuth/OIDC flow:

```text
email input → password page → OTP page → cross-origin redirect to att-yahoo.att.net → Yahoo inbox
```

Between password-auth and OTP verification, ATT's backend ties the pending authentication to a
session cookie or hidden state token. If Chrome discards or isolates that cookie between steps
(SameSite enforcement, cross-origin isolation, third-party cookie blocking), the OTP is submitted
against a session ATT can no longer locate -- validation fails with errorCode=908 even though the
6-digit code is correct.

Safari (WebKit) either handles the cross-origin session cookie more permissively for federated
login flows, or ATT's domain structure happens to satisfy WebKit's same-origin model. Either way,
the session state survives the OTP step under Safari.

### Consistency check against prior hypotheses

| Prior diagnosis                                          | Consistent?           | Notes                                                                                                                   |
|----------------------------------------------------------|-----------------------|-------------------------------------------------------------------------------------------------------------------------|
| "It's not you, it's us" (ATT ↔ Yahoo federation failure) | Separate failure mode | Prior = post-auth handoff; this = mid-auth OTP step                                                                     |
| Session corruption / identity collision                  | Not applicable        | 2026-06-20: auth reaches OTP, meaning identity was found and SMS was sent                                               |
| Account resolution failure                               | Not applicable        | OTP delivery implies ATT resolved the account                                                                           |
| Chrome password manager interference                     | Possible overlap      | Chrome PM may also interfere with session cookies; not directly relevant at OTP stage since OTP has no saved credential |

**New failure mode**: OTP validation rejected by ATT server (errorCode=908) specifically in Chrome.
Not seen in Safari. Not seen in any prior documented sessions.

### What changed (probable cause)

Chrome has progressively tightened third-party cookie and cross-origin session handling:

- Chrome 80 (2020): SameSite=Lax default; cross-site cookies require `SameSite=None; Secure`
- Chrome 115+ (2023): third-party cookie deprecation trial phase-in
- Chrome Privacy Sandbox: cross-origin session isolation

ATT's OAuth flow was designed before these restrictions. The OTP step likely relies on a session
cookie that Chrome now treats as cross-site and blocks or isolates. Safari has not enforced the
same deprecation timeline, so it still allows the session to persist across the flow.

This is consistent with ATT's pattern of not updating their auth implementation as browser
security evolves -- the same root cause as prior "voodoo fuckery" incidents.

### Implication for HOWTO_att_yahoo_login_v2.md

Workflow A in `HOWTO_att_yahoo_login_v2.md` specifies Chrome. As of 2026-06-20, Chrome fails
at OTP. Safari is the working browser path. The HOWTO should be updated to reflect Safari as
the recommended browser for browser-based att.net login.

### Actionable options if Chrome is required

1. Chrome → Settings → Privacy and security → Cookies → Allow all cookies
   (disables SameSite / third-party enforcement; try for ATT sessions only)
2. Add specific cross-site exception for `att.com` and `yahoo.com` in Chrome cookie settings
3. Use Chrome incognito -- sometimes behaves differently than a regular session with accumulated
   site data; worth one attempt before escalating
4. OR accept Safari as canonical att.net browser and update setup checklists

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
