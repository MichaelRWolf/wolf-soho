# Plan: Setup Fastmail with runningwolf.net Domain

## DONE ✅

- [x] Purchased 'runningwolf.net' domain from Porkbun
- [x] Subscribed to Fastmail 'Duo' level using account <michaelrwolf@fastmail.net>
- [x] Started adding 'runningwolf.net' domain to Fastmail
- [x] Updated nameservers at Porkbun to Fastmail's servers
- [x] Configured nameservers (ns1.messagingengine.com, ns2.messagingengine.com)
- [x] Verified configuration - Fastmail confirmed nameservers are working
- [x] Completed Fastmail setup - domain is ready for email use

## WIP

✅ **Step 1**: Updated nameservers at Porkbun to Fastmail's servers
✅ **Step 2**: Configured nameservers (ns1.messagingengine.com, ns2.messagingengine.com)
✅ **Step 3**: Verified configuration - Fastmail confirmed nameservers are working
✅ **Step 4**: Completed Fastmail setup - domain is ready for email use
⏳ **Step 4.5**: Disable web hosting (A records) - DNS page found, ready to configure

## TO DO

### Step 1: Update Nameservers at Porkbun
**Action:** Log in to Porkbun control panel
- Go to [porkbun.com](https://porkbun.com) and sign in
- Navigate to your domain management for 'runningwolf.net'
- Find the DNS/Nameserver settings section

### Step 2: Configure Nameservers
**Action:** Update nameserver settings to use Fastmail's servers
- Remove any existing nameserver entries
- Add exactly these two nameservers:
  - `ns1.messagingengine.com`
  - `ns2.messagingengine.com`
- Save the changes

### Step 3: Verify Configuration
**Action:** Check that changes have propagated
- Return to Fastmail setup page
- Click "**Check now**" button
- Wait for confirmation that nameservers are properly configured

### Step 4: Complete Fastmail Setup
**Action:** Finalize domain configuration
- Once nameservers are confirmed, Fastmail will complete the setup
- Domain should be ready for email use

### Step 4.5: Disable Web Hosting for runningwolf.net
**Action:** Ensure domain is email-only, no web hosting
- **Purpose**: Prevent any web traffic or hosting on the domain
- **Method**: Configure domain to reject web requests
- **Implementation**: 
  - In Fastmail domain settings, ensure no web hosting is enabled
  - If web hosting options exist, disable them
  - Domain should only respond to email-related requests (MX, SPF, etc.)
- **Verification**: 
  - Test that `http://runningwolf.net` returns no response or error
  - Test that `https://runningwolf.net` returns no response or error
  - Email functionality should remain unaffected

## Additional Setup Steps

### Step 5: Configure Email Addresses
**Action:** Set up email addresses for the domain
- Create primary email address (e.g., <michael@runningwolf.net>)
- Set up any additional email addresses needed
- Configure email forwarding if desired

#### 5.1: Create <michael@runningwolf.net>
**Action:** Set up primary email address
- In Fastmail web interface, go to Settings → Domains
- Select 'runningwolf.net' domain
- Click "Add Address" or "Create Email Address"
- Enter: `michael` (without @runningwolf.net)
- Set password for this email address
- Save the configuration

#### 5.2: Create <wendy@runningwolf.net>
**Action:** Set up secondary email address
- In same domain settings, click "Add Address" again
- Enter: `wendy` (without @runningwolf.net)
- Set password for this email address
- Save the configuration

#### 5.3: Test <michael@runningwolf.net>
**Action:** Verify primary email functionality
- Send test email from <michael@runningwolf.net> to another email address
- Send test email to <michael@runningwolf.net> from another email address
- Check both sent and received emails appear correctly
- Verify no delivery issues or spam folder placement

### Step 6: Test Email Functionality
**Action:** Verify email is working properly
- Send test email from new domain address
- Receive test email to new domain address
- Check spam folder if needed

#### 6.1: Test <wendy@runningwolf.net>
**Action:** Verify secondary email functionality
- Send test email from <wendy@runningwolf.net> to another email address
- Send test email to <wendy@runningwolf.net> from another email address
- Check both sent and received emails appear correctly
- Verify no delivery issues or spam folder placement

### Step 7: Configure Email Clients
**Action:** Set up email clients with new domain
- Update existing email clients (if any)
- Configure IMAP/SMTP settings:
  - IMAP: imap.fastmail.com (port 993, SSL)
  - SMTP: smtp.fastmail.com (port 587, STARTTLS)
- Test sending and receiving

#### 7.1: Configure <michael@runningwolf.net> in Mail.app
**Action:** Set up primary email in macOS Mail
- Open Mail.app on Mac
- Go to Mail → Add Account
- Select "Other Mail Account" (not iCloud, Gmail, etc.)
- Enter account details:
  - Name: Michael Wolf
  - Email: <michael@runningwolf.net>
  - Password: [password for michael@runningwolf.net]
- Click "Sign In"
- Mail.app should auto-detect Fastmail settings
- If not, manually configure:
  - Incoming Mail Server: imap.fastmail.com
  - Port: 993
  - Security: SSL
  - Outgoing Mail Server: smtp.fastmail.com
  - Port: 587
  - Security: STARTTLS
- Test sending and receiving emails

#### 7.2: Configure <michael@runningwolf.net> in Spark.app
**Action:** Set up primary email in Spark email client
- Open Spark.app on Mac
- Click "Add Account" or "+" button
- Select "Other" or "Custom IMAP"
- Enter account details:
  - Email: <michael@runningwolf.net>
  - Password: [password for michael@runningwolf.net]
- Spark should auto-detect Fastmail settings
- If not, manually configure:
  - IMAP Host: imap.fastmail.com
  - IMAP Port: 993
  - IMAP Security: SSL/TLS
  - SMTP Host: smtp.fastmail.com
  - SMTP Port: 587
  - SMTP Security: STARTTLS
- Test sending and receiving emails

#### 7.3: Configure <wendy@runningwolf.net> in Mail.app
**Action:** Set up secondary email in macOS Mail
- Open Mail.app on Mac
- Go to Mail → Add Account
- Select "Other Mail Account"
- Enter account details:
  - Name: Wendy Wolf
  - Email: <wendy@runningwolf.net>
  - Password: [password for wendy@runningwolf.net]
- Follow same configuration steps as <michael@runningwolf.net>
- Test sending and receiving emails

#### 7.4: Configure <wendy@runningwolf.net> in Spark.app
**Action:** Set up secondary email in Spark email client
- Open Spark.app on Mac
- Click "Add Account" or "+" button
- Select "Other" or "Custom IMAP"
- Enter account details:
  - Email: <wendy@runningwolf.net>
  - Password: [password for wendy@runningwolf.net]
- Follow same configuration steps as <michael@runningwolf.net>
- Test sending and receiving emails

#### 7.5: Test Webmail Access
**Action:** Verify webmail functionality for both users
- **Purpose**: Ensure webmail access works when email clients have issues
- **URL**: http://mail.runningwolf.net

##### 7.5.1: Test michael@runningwolf.net Webmail
**Action:** Verify primary user webmail access
- Navigate to http://mail.runningwolf.net
- Log in with michael@runningwolf.net credentials
- Verify webmail interface loads correctly
- Test sending email from webmail
- Test receiving email in webmail
- Verify all folders and settings are accessible

##### 7.5.2: Test wendy@runningwolf.net Webmail
**Action:** Verify secondary user webmail access
- Navigate to http://mail.runningwolf.net
- Log in with wendy@runningwolf.net credentials
- Verify webmail interface loads correctly
- Test sending email from webmail
- Test receiving email in webmail
- Verify all folders and settings are accessible

### Step 8: Set Up Email Aliases (Optional)
**Action:** Configure additional email addresses
- Common aliases: info@, admin@, webmaster@
- Set up catch-all address if needed
- Configure auto-replies if desired

### Step 9: Security and Backup
**Action:** Secure the email setup
- Enable two-factor authentication on Fastmail account
- Set up backup email addresses
- Configure account recovery options

### Step 10: Documentation
**Action:** Document the setup
- Record all email addresses created
- Document IMAP/SMTP settings
- Note any special configurations

## Troubleshooting Notes

### Common Issues
- **Nameserver propagation delay:** Can take up to 48 hours, but usually much faster
- **DNS cache issues:** Clear browser cache or try from different network
- **Email client configuration:** Double-check server settings and ports

### Porkbun-Specific Notes
- Porkbun typically has good DNS management interface
- Look for "DNS" or "Nameservers" section in domain management
- May need to remove default nameservers before adding Fastmail ones

## Resources

- [Fastmail Help Center](https://www.fastmail.com/help/)
- [Porkbun Domain Management](https://porkbun.com/account/domains)
- [Fastmail IMAP/SMTP Settings](https://www.fastmail.com/help/technical/servernamesandports.html)

---

**Image Summary:** The Fastmail setup page shows a clean interface with the heading
"Just a few more steps" and explains that email won't work until domain settings 
are
updated. It provides a two-step process: 1) Log into domain registrar control
panel,
and 2) Change nameservers to Fastmail's servers (ns1.messagingengine.com and
ns2.messagingengine.com). The page includes copy buttons for the nameserver addresses
and a "Check now" button to verify the configuration.
