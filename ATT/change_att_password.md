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
