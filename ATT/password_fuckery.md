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

Got it — you want a way to **leverage the fact that your iPhone is already logged in** to bypass AT\&T's broken sign-in process on your MacBook and Chrome, without triggering their "reset password" circus.

Here's the practical, minimal-frustration approach:

---

### 1. **Check if your iPhone can give you a "real" session cookie or token**

If your iPhone Mail app is still pulling messages, then AT\&T's IMAP/SMTP authentication is fine — it's just the *webmail* (via browser) and Mac Mail that are choking.

* On your iPhone, go to **Safari** and try to log in to [currently.att.yahoo.com](https://currently.att.yahoo.com) or [mail.yahoo.com](https://mail.yahoo.com).

  * If it works there, you now have an active browser session on your iPhone.
  * You can use **iCloud Keychain** to sync that saved password across devices — no retyping or re-entering required.
  * Sometimes, logging in via Yahoo's portal instead of AT\&T's triggers a working session that Mac Mail can then accept.

---

### 2. **Try "app-specific password" for the MacBook**

AT\&T/Yahoo sometimes blocks logins if they detect "older" mail clients. You can:

* In AT\&T/Yahoo account security settings (on iPhone Safari), create an **app password**.
* Use that app password in Mac Mail instead of your normal one.
  (This avoids AT\&T thinking the Mac is "suspicious.")

---

### 3. **Token-sharing workaround (cookies export)**

If you can get AT\&T Webmail working in Safari on your iPhone:

* Use a browser extension on Mac (like *EditThisCookie* in Chrome) to **import cookies** from the iPhone session.

  * You can export them on iPhone via **Safari Developer > Remote Automation** (requires enabling Web Inspector in iOS settings and connecting via USB to your Mac).
  * This gives Chrome the *exact same logged-in session*, skipping the password prompt.

---

### 4. **Use iCloud Keychain password sync**

If your iPhone already has the correct password saved in Safari/Keychain:

* Go to **System Settings > Apple ID > iCloud > Passwords & Keychain** on both devices — turn it on.
* Once synced, just choose the autofilled password on Mac Mail/Chrome instead of typing it.
* This prevents typos or "wrong password" rejections caused by AT\&T's janky login parser.

---

### 5. **Bypass AT\&T's own portal**

Sometimes AT\&T's own login page is down while Yahoo's backend is fine.

* Go straight to: [https://mail.yahoo.com](https://mail.yahoo.com)
  and use your full att.net email as username.
* If you can log in there on Mac, it will often start working in Mac Mail without changing passwords.

---

If you want, I can give you a **step-by-step for the "cookie transplant" trick** so your Chrome and Mac Mail think you're already logged in like your iPhone is — no password re-entry at all.

Do you want me to write that out? That's the most bulletproof way to avoid AT\&T's "password change" trap.
