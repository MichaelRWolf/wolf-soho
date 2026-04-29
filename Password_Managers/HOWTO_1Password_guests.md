# HOWTO: 1Password Guest Access for Shared Accounts

## Why Password Sharing Has Been Dangerous

For decades, security professionals advised **never share passwords** -- and for good reason:

- **No accountability** -- when everyone knows the password, no one is responsible for it
- **No revocation** -- removing access for one person means changing the password for everyone
- **Insecure transmission** -- passwords shared via email, text, or sticky notes travel in plaintext
- **Credential rot** -- shared passwords get simplified ("make it something easy to remember") and never rotated
- **Blast radius** -- one person's phishing incident or data breach compromises everyone's access
- **No audit trail** -- no way to know who logged in, when, or from where

The result: organizations either locked down access so tightly that collaboration suffered, or they shared credentials so loosely that security was theater.

## How 1Password Changes the Equation

1Password doesn't eliminate shared access -- it makes shared access *safe*:

| Old Way                       | 1Password Way                                        |
|-------------------------------|------------------------------------------------------|
| Email the password            | Each person has their own encrypted vault            |
| Change password to revoke     | Remove guest; their access is gone instantly         |
| Memorize a weak password      | Strong, random passwords -- nobody memorizes them    |
| Plaintext transmission        | End-to-end encrypted; 1Password never sees your data |
| No audit trail                | Each account has its own login identity              |
| One breach = everyone exposed | Guest accounts are isolated; breach is contained     |

The key insight: **guests access the vault, not the password.** They use 1Password to fill credentials -- they never need to see or handle the raw password at all.

---

## Our Setup (Michael & Wendy)

**Plan:** 1Password Families (billed annually)

**Current usage:**

| Slot Type      | Used               | Available |
|----------------|--------------------|-----------|
| Family Members | 2 (Michael, Wendy) | 3 more    |
| Guests         | 0                  | 5 more    |

**Shared vault:** `Shared-BLOOM`

**Invited guests:** Amber, Jill, Jeff

**Guest access model:** Each guest gets their own 1Password account and can access only the `Shared-BLOOM` vault -- no other family vaults are visible to them.

---

## HOWTO: Admin (Michael or Wendy)

### Invite a Guest

1. Go to [1password.com](https://1password.com) and sign in
2. Click **Manage** in the left sidebar → **People**
3. Click **Invite People**
4. Enter the guest's email address; set role to **Guest**
5. Under vault access, select **Shared-BLOOM** only
6. Click **Send Invitation**
7. Repeat for each guest (Amber, Jill, Jeff)

### Grant or Change Vault Access for an Existing Guest

1. **Manage** → **People** → click the guest's name
2. Under **Vault Access**, add or remove vaults
3. Changes take effect immediately

### Revoke a Guest's Access

1. **Manage** → **People** → click the guest's name
2. Click **Remove from family**
3. Their account is deactivated; they can no longer access any vault

### Add or Update an Item in Shared-BLOOM

1. Open 1Password (app or browser)
2. Select the **Shared-BLOOM** vault from the vault list
3. Click **+** to add a new item, or click an existing item to edit
4. Changes sync to all guests automatically

### Who Has Access to a Vault?

Access is managed at the **vault level** -- individual items do not have separate permissions.

**To see who can access a vault:**

1. Go to [1password.com](https://1password.com) → **Vaults** in the left sidebar
2. Click the vault name (e.g., **Shared-BLOOM**)
3. The vault detail page lists everyone with access and their permission level

**To see which vaults a specific person can access:**

1. **People** → click the person's name
2. Their profile lists every vault they have access to

**To know who can see a specific item:** check which vault it lives in, then check that vault's access list. There is no item-level access control on the Families plan.

---

## HOWTO: Member (Michael or Wendy -- daily use)

### Access Shared-BLOOM

1. Open the 1Password app or browser extension
2. In the vault selector (top-left), choose **Shared-BLOOM**
3. Browse or search for the item you need

### Use a Saved Login

1. Navigate to the site in your browser
2. Click the 1Password icon in the toolbar (or use **Cmd+\\** on Mac)
3. Select the matching login -- 1Password fills username and password automatically

### Add a New Shared Login

1. When creating a new account on a website, let 1Password suggest a strong password
2. Save it directly to **Shared-BLOOM** (choose vault before saving)
3. All guests with access will see it immediately

---

## HOWTO: Guest (Amber, Jill, Jeff)

### Accept the Invitation and Set Up Your Account

1. Check your email for an invitation from 1Password
2. Click **Accept Invitation**
3. You'll be prompted to create a **Master Password** -- choose something strong that you will remember; 1Password cannot recover it for you
4. Download the **Emergency Kit** PDF and store it somewhere safe (printed copy recommended)
5. Install the 1Password app or browser extension on your device(s)

### Sign In to 1Password

1. Open the 1Password app or go to [1password.com](https://1password.com)
2. Enter the **1Password account URL** (shown in your invitation email, e.g. `my.1password.com`)
3. Enter your email address and Master Password
4. You will see only the **Shared-BLOOM** vault

### Log Into a Shared Account -- Method 1: Autofill (Example: <WendyRWolf.BLOOM@gmail.com>)

1. Go to [gmail.com](https://gmail.com) in your browser
2. Click the **1Password icon** in the browser toolbar (install the extension if not already installed: [1password.com/downloads](https://1password.com/downloads))
3. 1Password will suggest the matching login -- click it
4. Username (`WendyRWolf.BLOOM@gmail.com`) and password fill automatically
5. Click **Sign in** on the Gmail page

> You never need to see or type the password. 1Password handles it.

### Log Into a Shared Account -- Method 2: Copy and Paste (Example: <WendyRWolf.BLOOM@gmail.com>)

Use this when autofill doesn't work (some sites block it) or the browser extension isn't installed.

1. Open the 1Password app
2. Find the `WendyRWolf.BLOOM@gmail.com` login item in **Shared-BLOOM**
3. Click the item to open it
4. Click the **copy icon** next to the username field -- it copies to your clipboard
5. Go to [gmail.com](https://gmail.com), click the email field, paste (**Cmd+V** on Mac, **Ctrl+V** on Windows)
6. Back in 1Password, click the **copy icon** next to the password field
7. Click the password field on Gmail, paste
8. Click **Sign in**

> The password is on your clipboard briefly -- 1Password clears it automatically after 90 seconds.

### Install the Browser Extension

- **Chrome/Brave/Edge:** [Chrome Web Store -- 1Password](https://chrome.google.com/webstore/detail/1password/aeblfdkhhhdcdjpifhhbdiojplfjncoa)
- **Firefox:** [Firefox Add-ons -- 1Password](https://addons.mozilla.org/en-US/firefox/addon/1password-x-password-manager/)
- **Safari:** Included with the 1Password Mac app

After installing, sign in with your 1Password account credentials.

### Install on iPhone or Android

1. Search **1Password** in the App Store or Google Play
2. Sign in with your account credentials
3. Enable **AutoFill Passwords** in your device settings when prompted
4. 1Password will offer to fill credentials whenever you open a supported app or website

### What You Can and Cannot Do as a Guest

| Action                                     | Guest                                            |
|--------------------------------------------|--------------------------------------------------|
| View items in Shared-BLOOM                 | Yes                                              |
| Use autofill for shared logins             | Yes                                              |
| Add new items to Shared-BLOOM              | No (read-only unless admin grants edit access)   |
| See Michael & Wendy's Private vaults       | No                                               |
| Change your Master Password                | Yes (your account, your password)                |
| Share your guest account with someone else | No -- each person needs their own invitation     |
| Reveal a password in plain text            | Yes -- click the eye icon on any item to show it |
| Copy a password to clipboard               | Yes -- available on any item                     |
