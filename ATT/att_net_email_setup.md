# Setting up ATT.NET Email on iPhone and MacBook (2025)

This guide explains how to configure your legacy `@att.net` email
account on iOS and macOS **using Secure Mail Keys (SMKs)** instead of
your regular password. This ensures a stable, secure, and OAuth-free
setup.

---

##

SMKs

| email account          | Name                                       | Date       | Device        |
|------------------------|--------------------------------------------|------------|---------------|
| <michaelrwolf@att.net> | SMK - <michaelrwolf@att.net> iPhone SE 3rd | 2025-05-16 | iPhone SE 3/e |

## 🔍 Overview: Why Use "Other" Instead of "Yahoo"

| Option       | Use SMK? | Reliable? | Avoid lockouts? | Recommendation |
|--------------|----------|-----------|-----------------|----------------|
| Yahoo        | ❌        | ❌         | ❌               | **Avoid**      |
| Other (IMAP) | ✅        | ✅         | ✅               | **Use this**   |

> **Reminder**: Selecting **Yahoo** triggers an **OAuth login flow**,
> which bypasses Secure Mail Keys. This often causes login failures or
> account lockouts on older or multiple devices. Only "Other" supports
> SMK-based manual configuration.

---

## ✅ Prerequisites

- An active `@att.net` email account
- A **Secure Mail Key** (see instructions below)
- 1Password or similar password manager

---

## 🔐 Create a Secure Mail Key (SMK)

📚 References

- AT&T. (n.d.). Create a secure mail key. AT&T Support.
[https://www.att.com/support/article/email-support/KM1240308/](https://www.att.com/support/article/email-support/KM1240308/)

1. Go to
   [https://www.att.com/my/#/profile/signin-info](https://www.att.com/my/#/profile/signin-info)
   and log in.
2. Scroll to the **Sign-in Info** section.
3. Under **Email**, click **Manage secure mail key**.
4. Click **Add Secure Mail Key**
   - Name it: `SMK - michaelrwolf@att.net iPhone SE 3rd Edition`
   - Click **Create Secure Mail Key**
   - **Copy the 16-character key** immediately -- it won't be shown again.

---

## 💾 Save the SMK in 1Password

### If You Have a Login Item for AT&T

- Edit the existing entry.
- Add a new section (e.g., "Secure Mail Keys").
- Add a field labeled: `SMK - michaelrwolf@att.net iPhone SE 3rd`, and
  paste the key.

### If Not

- Create a new **Login** item.
  - Title: `AT&T Secure Mail Keys`
  - Username: `yourname@att.net`
  - Add a section: "Secure Mail Keys"
  - Add the SMK field and paste the key.

---

## 📱 iPhone Setup: Manual (IMAP) Using SMK

1. Go to: **Settings > Mail > Accounts > Add Account > Other > Add Mail Account**
2. Enter:
   - **Name**: Your name
   - **Email**: `yourname@att.net`
   - **Password**: (your **Secure Mail Key**)
   - **Description**: AT&T Mail
3. Incoming Mail Server:
   - Host: `imap.mail.att.net`
   - Username: `yourname@att.net`
   - Password: (SMK)
4. Outgoing Mail Server:
   - Host: `smtp.mail.att.net`
   - Username: `yourname@att.net`
   - Password: (SMK)
5. Tap **Save**
6. Verify Advanced Settings:
   - IMAP Port: 993, SSL: On
   - SMTP Port: 465 (or 587), SSL: On

---

## 💻 MacBook Setup: Apple Mail

1. Open **Mail > Settings > Accounts**
2. Click **+** to add new account
3. Select **Other Mail Account**
4. Enter:
   - Name, Email (`@att.net`), and **SMK as password**
5. Configure Incoming and Outgoing Mail Servers (as above)

---

## 🧠 Tip: Use Separate SMKs Per Device (Optional)

To avoid full lockout if one device fails:

- Create unique SMKs (e.g., one for iPhone, one for Mac)
- Name them clearly
- Track them in 1Password

---

## 🛑 Avoid This

- **Do not use Yahoo button**
- **Do not use your real AT&T password**
- **Do not reuse one SMK across all devices if you've experienced lockouts**

---

Stay resilient!
