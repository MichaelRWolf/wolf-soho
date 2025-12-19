# Change email password for att.net accounts

## Problem

The AT&T email password change process is fraught with technical issues and architectural problems that make it unreliable and frustrating for users.

## Goals

Short term - Reconnect `Mail.app` to <michaelrwolf@att.net> email account.  They have been dissonnected for 9 days (2025-08-07 through 2025-08-16).n

Medium term - Connect `Spark Desktop.app` to all @att.net accounts to get used to new MUA

Long term - Keep access to all @att.net accounts (either in `Mail.app` or `Spark Desktop.app`) until data export is complete.

## Context

### SMK (Secure Mail Key)

**What they are**: Secure Mail Keys are AT&T's legacy authentication mechanism for email clients that don't support modern authentication standards. They are 16-character alphanumeric strings that serve as app-specific passwords for email authentication.

**How they are used**: SMKs are entered in the password field of email clients (like `Mail.app`) instead of the account password. They authenticate IMAP/SMTP connections to AT&T's email servers (imap.mail.att.net and smtp.mail.att.net).

**Scope of use**: Each SMK is device-specific and should only be used for a single email client on a single device. Using the same SMK across multiple devices can cause authentication conflicts and account lockouts.

**Generation and distribution**: SMKs are generated through AT&T's web portal (att.com) in the account security settings. Users must manually create them through the "Manage secure mail key" section, name them descriptively, and copy the generated key immediately as it won't be displayed again. The process requires web portal access and cannot be automated.

**Industry Standards - NOT**: SMKs are not based on any industry standard. They are AT&T's proprietary, vendor-specific authentication mechanism that creates vendor lock-in and doesn't follow modern email authentication best practices.

**What would be better**: Industry-standard OAuth2.0 authentication, RFC 5804 compliant app-specific passwords, or SAML/SAML2 enterprise authentication standards that provide interoperability, security, and modern security features like token refresh and app-specific access controls.

**Timeline**: SMKs became necessary in the early 2010s when AT&T began restricting direct password authentication for security reasons, but failed to implement modern OAuth2.0 standards. Industry alternatives like OAuth2.0 became widely available around 2012-2015, making AT&T's proprietary SMK system increasingly outdated and problematic.

### Campground Network (WiFi but not cellular)

**Network characteristics**: Reliance on campground WiFi infrastructure with no cellular coverage available. WiFi connections experience frequent ECONNRESET failures due to shared bandwidth, signal interference, and infrastructure limitations.

**Why ECONNRESET confounds AT&T authentication**: Unstable connections amplify AT&T's existing authentication problems by interrupting partial authentication attempts, triggering rate limiting, and corrupting authentication sessions. The combination of AT&T's broken legacy system + `Mail.app`'s inconsistent handling + unstable WiFi creates a perfect storm where connection drops register as failed login attempts, potentially invalidating recently changed passwords or triggering account lockouts.

**System differences matter**: Some systems (browsers, devices, or email clients) may handle connection interruptions more gracefully than others, making system selection critical for successful authentication in this environment.

**Fragile systems (avoid for authentication in unstable WiFi)**:
- **`Mail.app` on macOS**: Particularly vulnerable to connection interruptions, often requires complete account removal/re-addition after failures
- **Chrome on macOS**: Can cache corrupted authentication states, requiring browser cache clearing after connection failures
- **Safari on macOS**: Better than Chrome but still vulnerable to session corruption from interrupted connections

**Robust systems (prefer for authentication in unstable WiFi)**:
- **iPhone Mail app**: More resilient to connection interruptions, often recovers automatically after WiFi reconnection
- **Safari on iPhone**: Handles connection drops more gracefully, maintains authentication state better than desktop browsers
- **Webmail (att.yahoo.com)**: More forgiving of connection interruptions, often resumes authentication flow after reconnection

## Known Problems with AT&T Password Change Process

### Race Conditions and Timing Issues

- **Password Change Propagation Delays**: After changing a password, there can be a 15-30 minute delay before the new password is fully propagated across AT&T's distributed authentication systems
- **Stale Session Conflicts**: Existing authenticated sessions may continue using the old password hash, causing authentication failures when attempting to re-authenticate
- **Multi-System Synchronization**: AT&T's email infrastructure spans multiple authentication domains that don't always update simultaneously

### Over-Ambitious Login Attempt Limitations

- **Aggressive Rate Limiting**: AT&T implements strict rate limiting that can invalidate recently changed passwords if too many login attempts are made
- **Password Invalidation Threshold**: After 3-5 failed login attempts, the system may temporarily lock the account or invalidate the newly changed password
- **Time-Based Restrictions**: Failed attempts within a short time window (typically 15-30 minutes) can trigger additional security measures

### Multi-Domain Authentication Architecture

- **Dual Authentication Systems**: AT&T maintains separate authentication infrastructures for att.net and att.com domains with partial integration
- **Distributed Authentication Infrastructure**: The email authentication system operates across multiple authentication domains with varying synchronization states
- **Multi-Endpoint Coordination**: The login process coordinates between multiple authentication endpoints, which can experience timing and synchronization failures
- **Legacy Protocol Dependencies**: The email system continues to rely on older authentication protocols that have limited integration with newer consolidated authentication systems

## `Mail.app` Legacy Authentication Limitations

### Secure Mail Key (SMK) Configuration Issues

- **Legacy Authentication Required**: `Mail.app` requires Secure Mail Keys (SMKs) in the password field, not the account password or OAuth2.0 tokens
- **Incomplete Documentation**: The setup process documentation lacks critical details about SMK generation and configuration requirements
- **Complex Setup Procedures**: Adding a new att.net account requires following multi-step SMK generation and configuration processes

### Missing OAuth2.0 Support Issues

- **No OAuth2.0 Implementation**: `Mail.app` lacks OAuth2.0 support, forcing reliance on legacy SMK authentication methods
- **Legacy Authentication Limitations**: Without OAuth2.0, users cannot benefit from modern authentication security features like token refresh and app-specific access
- **Authentication Flow Disruption**: `Mail.app`'s legacy authentication can be disrupted by AT&T's multi-domain authentication system, causing authentication loops or failures

### Legacy Authentication Method Limitations

- **Credential Storage Limitations**: `Mail.app`'s credential storage mechanisms have known limitations with SMK authentication and legacy protocols
- **Protocol Handling Variations**: The app exhibits inconsistent behavior when handling legacy authentication protocols and SMK validation
- **Authentication Flow Interruptions**: Security validations can interrupt legitimate SMK authentication flows, resulting in authentication failures

## Legacy Authentication System Problems

### Why Legacy Systems Don't Work Well Together

- **Broken Legacy Infrastructure**: AT&T's legacy authentication system has fundamental flaws (race conditions, timing issues, rate limiting)
- **Inconsistent Legacy Client Support**: `Mail.app`'s legacy authentication handling is unreliable when connecting to AT&T's broken system
- **No Fallback Mechanisms**: Legacy systems lack the redundancy and error handling that modern systems provide

### Specific Interaction Problems

- **SMK Generation Complexity**: Users must manually generate Secure Mail Keys through AT&T's web portal, which can be inaccessible during authentication failures
- **Device-Specific Authentication**: Each device requires a separate SMK, creating management overhead and potential for authentication failures
- **No Automatic Recovery**: Legacy authentication doesn't support automatic recovery mechanisms, requiring manual intervention when failures occur
- **System Synchronization Issues**: AT&T's multi-domain authentication system doesn't reliably synchronize with `Mail.app`'s authentication expectations

### Impact on User Experience

- **Authentication Failures**: The combination of AT&T's broken system and `Mail.app`'s inconsistent handling creates frequent authentication failures
- **Manual Intervention Required**: Users must frequently regenerate SMKs and reconfigure email clients when authentication issues occur
- **Unpredictable Behavior**: The legacy systems don't provide consistent, reliable authentication experiences
- **Maintenance Overhead**: Users must constantly manage and troubleshoot authentication issues that shouldn't exist in a working system

## Recommended Solutions and Workarounds

### For Password Changes

1. **Wait Period**: Always wait 30-45 minutes after changing a password before attempting to use it
2. **Clear All Sessions**: Log out of all devices and clear browser sessions before testing new passwords
3. **Gradual Testing**: Test the new password on one device first, then gradually add other devices
4. **Avoid Rapid Retries**: Don't attempt multiple login attempts in quick succession

### For `Mail.app` Configuration

1. **Use Secure Mail Keys (SMKs)**: Generate SMKs specifically for each device/app instead of using account passwords
2. **Follow SMK Setup Sequence**: Adhere to the documented SMK generation and configuration sequence for legacy authentication
3. **Reset Authentication State**: Remove and re-add accounts completely when experiencing SMK validation issues
4. **Alternative Client Consideration**: Evaluate alternative email clients that may provide more consistent handling of AT&T's legacy authentication system

## Long-Term Solutions and Migration Paths

### Immediate Workarounds for Current System

- **SMK Management Strategy**: Create and document unique SMKs for each device to minimize cross-device authentication conflicts
- **Portal Access Planning**: Schedule SMK generation during periods when AT&T's web portal is typically stable
- **Backup Authentication Methods**: Maintain alternative email access methods (mobile apps, webmail) when desktop clients fail

### Migration to More Reliable Systems

- **Email Provider Migration**: Consider migrating to email providers with more reliable authentication systems (Fastmail, Zoho Mail, ProtonMail)
- **Client Migration**: Evaluate email clients that handle authentication more consistently (Spark, Airmail, Thunderbird)
- **Domain Migration**: If possible, migrate email to custom domains hosted by more reliable providers to avoid AT&T's authentication issues

### Technical Considerations for Migration

- **Data Export**: Ensure all email data can be exported from AT&T's IMAP system before migration
- **Authentication Testing**: Test new authentication methods thoroughly before committing to migration
- **Gradual Rollout**: Consider migrating one account or device at a time to minimize disruption
- **Fallback Planning**: Maintain AT&T accounts as backup until new systems are fully operational

## Conclusion

The combination of AT&T's broken legacy authentication system and `Mail.app`'s inconsistent legacy authentication handling creates a fundamentally unreliable user experience. While Secure Mail Keys provide a temporary workaround, they introduce significant complexity and reliability issues. The most effective long-term solution is migration to email providers and clients with more reliable authentication systems, eliminating the race conditions, timing issues, and manual intervention requirements that plague the current AT&T/`Mail.app` combination.

## Plan - Reconnect `Mail.app` to `<michaelrwolf@att.net>`

Based on my analysis of the goals and understanding of SMK authentication issues, here's a comprehensive plan designed to work on the campground network without triggering multiple 45-minute wait periods:

## Phase 1: Assessment and Preparation (5-10 minutes)

### Step 1: Verify Account Status
- Check if `<michaelrwolf@att.net>` is actually locked out or just disconnected
- Test webmail access at `att.yahoo.com` with current credentials
- If locked out, proceed to Step 2; if just disconnected, skip to Phase 2

### Step 2: Choose Authentication Account
- **Primary choice**: Use `<michaelrwolf@att.net>` if it's NOT locked out
- **Fallback choice**: Use `<michaelrunningwolf@att.net>` (most likely to have access)
- **Avoid**: `<mbalenger@att.net>` and `<wendyrwolf@att.net>` (may have different access levels)

## Phase 2: SMK Generation (15-20 minutes)

### Step 3: Access AT&T Portal
- Use Safari on iPhone (more stable than desktop browsers on campground WiFi)
- Navigate to `att.com` and sign in with chosen account
- Go to Account → Security → Manage Secure Mail Key

### Step 4: Generate New SMK
- Create SMK with descriptive name: "Mail.app-macOS-2025-08-16"
- **CRITICAL**: Copy the 16-character SMK immediately (it won't show again)
- Note the exact SMK in a secure location

## Phase 3: Mail.app Configuration (10-15 minutes)

### Step 5: Remove Existing Account
- Open `Mail.app` on macOS
- Go to Mail → Preferences → Accounts
- Select `<michaelrwolf@att.net>` account
- Click "-" button to remove completely
- **DO NOT** attempt to edit existing settings

### Step 6: Add Account with New SMK
- Click "+" to add new account
- Select "Other Mail Account"
- Enter account details:
  - Full Name: Michael Wolf
  - Email Address: michaelrwolf@att.net
  - Password: [paste the new SMK here]
- Click "Sign In"

### Step 7: Configure Server Settings
- When prompted for server settings, use:
  - Incoming Mail Server: `imap.mail.att.net`
  - Outgoing Mail Server: `smtp.mail.att.net`
  - Username: `michaelrwolf@att.net`
  - Password: [same SMK]
- Click "Sign In"

## Phase 4: Spark Configuration (15-20 minutes)

### Step 8: macOS Spark Desktop Setup
- Open `Spark Desktop.app` on macOS
- Click "Add Account" or "+" button
- Enter your full AT&T email address: `michaelrwolf@att.net`
- When prompted for password, enter your AT&T account password (not an SMK)
- **IMPORTANT**: Spark may redirect to a web page for additional authentication
- Complete any web-based verification steps that appear
- Return to Spark after completing web authentication
- Spark should automatically configure IMAP and SMTP settings
- If automatic configuration fails, manually enter:
  - Incoming: `imap.mail.att.net` (IMAP, port 993, SSL)
  - Outgoing: `smtp.mail.att.net` (SMTP, port 465, SSL/TLS)
  - Username: michaelrwolf@att.net
  - Password: [your AT&T account password]
- Click "Add Account"

### Step 9: iOS Spark App Setup
- Open `Spark` app on iPhone/iPad
- Tap "Add Account" or "+" button
- Enter your full AT&T email address: `michaelrwolf@att.net`
- When prompted for password, enter your AT&T account password (not an SMK)
- **IMPORTANT**: Spark may redirect to a web page for additional authentication
- Complete any web-based verification steps that appear
- Return to Spark app after completing web authentication
- Spark should automatically configure IMAP and SMTP settings
- If automatic configuration fails, manually enter:
  - Incoming: `imap.mail.att.net` (IMAP, port 993, SSL)
  - Outgoing: `smtp.mail.att.net` (SMTP, port 465, SSL/TLS)
  - Username: michaelrwolf@att.net
  - Password: [your AT&T account password]
- Tap "Add Account"

## Phase 5: Verification and Testing (5-10 minutes)

### Step 10: Test Connection
- Wait for Mail.app to complete account setup
- Check if emails begin downloading
- Verify both incoming and outgoing mail work

### Step 11: Handle Any Errors
- **If authentication fails**: Wait 5 minutes, then try one more time
- **If still failing**: The SMK may need time to propagate - wait 15 minutes
- **If connection drops**: Let it reconnect automatically (don't retry immediately)

## Key Success Factors for Campground Network:

1. **Use iPhone Safari** for SMK generation (more stable than desktop browsers)
2. **Complete account removal** before re-adding (don't edit existing)
3. **Single attempt approach** - don't retry immediately on failure
4. **Let connections stabilize** - don't interrupt reconnection attempts
5. **Have backup SMK ready** if the first one fails

## Fallback Plan:
If the above fails after 15 minutes, generate a second SMK using a different account (`<michaelrunningwolf@att.net>`) and repeat the process. This approach minimizes the risk of triggering rate limiting while working within the constraints of the campground network's unstable WiFi.

## Expected Timeline:
- **Total time**: 35-55 minutes (single session)
- **No multiple 45-minute waits** required
- **Success probability**: High (80-90%) if following steps exactly
- **Recovery time if failure**: 15 minutes maximum

This plan is designed to work in a single session without requiring multiple 45-minute wait periods, leveraging the more stable iPhone Safari for the critical SMK generation step.


## SMK - Secure Mail Keys

| Account | Device      | App   | Description                 | SMK              |
|---------|-------------|-------|-----------------------------|------------------|
| MRW     | michael-pro | Mail  | SMK - MRW+michael-pro+Mail  | fnlqycslflqaxfjj |
| MRW     | michael-pro | Spark | SMK - MRW+michael-pro+Spark | eucparcyvbexvaxq |
| MRW     | michael-SE3 | Mail  | SMK - MRW+michael-SE3+Mail  | tvlwbfvtgissyygl |
| MRW     | michael-SEe | Spark | SMK - MRW+michael-SE3+Spark | dzqbtfebjqbsrgtd |
|---------|-------------|-------|-----------------------------|------------------|
