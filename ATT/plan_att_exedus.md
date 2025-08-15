# plan_att_exedus.md

## Past 10--20 Years --- Problems with @att.net

1. **Zero support**
    - Since AT&T made it free, they've given exactly \$0 worth of
        service and support.\
2. **Account tied to ISP**
    - Locked to AT&T/Yahoo backend whims with no provider choice.\
3. **Random service breaks**
    - Working on one device, failing on others, with no fix path
        except waiting or changing passwords.\
4. **Password-change cascades**
    - Change → update everywhere → sometimes change again within
        hours.\
5. **Opaque operations**
    - No service status, no logs, no admin control.\
6. **No roadmap or improvement**
    - Treated as a cost sink, not a real product.

## Next 10--20 Years --- Vision for Mail Hosting

1. **Provider independence**
    - Email address not tied to an ISP or big ecosystem;
        **RunningWolf.net** becomes the permanent identity.\
2. **Professional-grade reliability**
    - Hosted by experts (IaaS-level managed service), not self-run
        hardware.\
3. **Standards-compliant access**
    - Smooth IMAP/SMTP for Mail.app, no lockouts or forced webmail.\
4. **Transition safety net**
    - @att.net forwards to the new address during a controlled
        migration.\
5. **Security without chaos**
    - MFA, app passwords, passkeys that don't throw every device
        offline.\
6. **Archival and export**
    - Full data control; the host provides reliable export tools to
        leave at any time.\
7. **Longevity**
    - Service likely to exist and stay standards-compliant into the
        2040s.
8. Use cases
    Shared domain name with separate email addresses for <michael@example.com> and <wendy@example.com>
    Shared email account for shared services (e.g. bank, amazon, netflix), possibly <shared-service@example.com> or <becu-login@example.com>
    Possible sub-domain in future for different business iniatives - MichaelPassionProject.example.com
    Start with email migration away from @att.net
    Possibly move hosted web sites to new domain
    Start out using this new domain and service for personal email.  Have migration plan to extend it to professional email.

## Data Migration Options (25+ years of mail)

## Migration Options

### Full Migration

**Description:** Copy every message + folder into new provider

**Pros:**

- All history searchable in one place

**Cons:**

- Larger mailbox cost
- More time to transfer

**Typical Cost:** $0--$100 one-time if DIY; $200--$500 if hiring migration service

### Partial Migration

**Description:** Move only recent mail (e.g., last 1--3 years)

**Pros:**

- Lower storage cost
- Faster migration

**Cons:**

- Old mail stays separate
- Requires legacy access

**Typical Cost:** $0--$50 if DIY

### Archive + Clean Start

**Description:** Export old mail to .mbox and store offline; new inbox starts empty

**Pros:**

- No ongoing hosting cost for old mail
- Fastest new setup

**Cons:**

- Searching old mail is clunkier
- Requires opening archives separately

**Typical Cost:** $0--$50 for storage

## Clarifications

- **Self-host vs IaaS**: Self-host = your server, your electric bill,
    your patching headaches → ruled out. IaaS email hosting = paying a
    provider to run it for you on their hardware.
- **Decoupling from iCloud/Gmail/Outlook.com**: You can still read
    mail in any client, but the mailbox lives on RunningWolf.net's
    provider.
- **Archival strategy**: Decide if your email provider is your
    long-term archive or if you keep historical archives offline.

## Coupling domain name registrar and email host

### Domain Name Registrars

Recommended providers:

- Namecheap - Competitive pricing, good UI, strong reputation -- Yes
- Google Domains - Simple interface, integrates well with other Google services
- Cloudflare - Very competitive pricing, excellent security features -- NO
- GoDaddy - Well-known, extensive features but more aggressive upselling

### Email Hosting Providers

Recommended providers:

- MXroute - Excellent value, multiple domains allowed, technical setup required
- Fastmail - Great interface, custom domain support, strong privacy focus
- Zoho Mail - Affordable, includes business tools, can be complex to set up
- Microsoft 365 - Full Office suite included, enterprise-grade but costlier
- ProtonMail - End-to-end encryption, privacy focused, premium pricing

Non-starters:
- Microsoft 365
- Premium pricing (therefore ProntoMail)
- Google
- Technical setup required

#### Important Considerations

Server - Important for mail service provider (MTA) - to handle RunningWolf.net
- No "technical setup" requirement.  We do NOT want to be 1995 system administrators to do everything.
- MUST allow multiple domains for email
- MUST allow sub-domains for email

App - Important for MUA (Mail User Agent) like Mail.app (on macBook) or xxx (on iPHone)

**Security & Privacy:**

- What level of encryption do they offer? (end-to-end, at-rest, in-transit) -> ???
- Do they scan your email for advertising/targeting? -> ???
- What's their data retention policy? -> ???
- Where are their servers located? (jurisdiction matters for privacy laws) -> ???

**Reliability & Support:**

- What's their uptime guarantee? -> ???
- Do they offer 24/7 support? -> ???
- How quickly do they respond to support requests? -> ???
- Do they have a good reputation for reliability? -> ???

**Features & Compatibility:**

- Do they support IMAP/SMTP for all email clients? -> ???
- Do they offer OAuth 2.0 authentication? -> ???
- Can you use your own domain name? -> ???
- Do they offer calendar and contact sync? -> ???

**Cost & Storage:**

- What's the monthly/yearly cost? -> ???
- How much storage is included? -> ???
- What are the costs for additional storage? -> ???
- Are there any hidden fees or setup costs? -> ???

**Migration & Import:**

- Do they provide migration tools from AT&T? -> ???
- Can you import .mbox files? -> ???
- Do they offer migration assistance? -> ???
- How long does migration typically take? -> ???

**Usability:**

- Do they have a modern webmail interface? -> ???
- Does it work well with Apple Mail and other clients? -> ???
- Is the interface intuitive and easy to navigate? -> ???
- Do they offer mobile apps? -> ???
- Good rule system for incoming mail.  Something that is text based instead of relying on middle schoolers to design a clickey-clickey interface.
- (Optional) Auto-reactive rule based system that observes your behavior and operates to do rule-ish moving or viewing.

### Using Same Provider vs Separate Providers

Pros of Using Same Provider:

- Simplified billing and account management
- Potentially easier initial setup
- Often includes package discounts
- Single support contact

Cons of Using Same Provider:

- Less flexibility to change services independently
- May compromise on quality of one service
- Often more expensive than best-of-breed choices
- Risk of vendor lock-in
- Email migration becomes tied to domain transfer timing

#### Hosting Providers - Backend Features

| Vendor     | OAuth 2.0 | Custom Domain | Multiple Domains | Storage | Cost/Month | Mobile Apps | Calendar | Contacts | Overall Rank | Notes                                   |
|------------|-----------|---------------|------------------|---------|------------|-------------|----------|----------|--------------|-----------------------------------------|
| Fastmail   | ✅ Yes    | ✅ Yes        | ✅ Yes           | 2-25GB  | $3-5       | ✅ Yes      | ✅ Yes   | ✅ Yes   | 1st          | Best features, modern interface         |
| Zoho Mail  | ✅ Yes    | ✅ Yes        | ✅ Yes           | 5-50GB  | $1-4       | ✅ Yes      | ✅ Yes   | ✅ Yes   | 2nd          | Good features, affordable               |
| ProtonMail | ✅ Yes    | ✅ Yes        | ✅ Yes           | 5-500GB | $4-8       | ✅ Yes      | ✅ Yes   | ✅ Yes   | 3rd          | Privacy-focused, higher cost            |
| MXroute    | ❌ No     | ✅ Yes        | ✅ Yes           | 10-50GB | $2-7       | ❌ Limited  | ❌ No    | ❌ No    | 4th          | Basic features, technical setup         |
| Namecheap  | ❌ No     | ✅ Yes        | ✅ Yes           | 10GB    | $2.88      | ❌ Limited  | ❌ No    | ❌ No    | 5th          | Basic features, no OAuth 2.0            |
| AT&T       | ❌ No     | ❌ No         | ❌ No            | 1GB     | $0         | ✅ Yes      | ❌ No    | ❌ No    | 6th          | Degraded service, authentication issues |

#### Hosting Providers - Webmail Features

#### Hosting Providers - Rules

| Vendor     | Rule Interface | Text-based Rules | Visual Builder | Version Control | Mail.app Integration | Overall Rank | Notes                                   |
|------------|----------------|------------------|----------------|-----------------|----------------------|--------------|-----------------------------------------|
| Fastmail   | ✅ Dual-pane   | ✅ Full Sieve    | ✅ Drag & drop | ✅ Internal     | ✅ OAuth 2.0         | 1st          | Modern dual-interface, best rule system |
| Zoho Mail  | ❌ GUI only    | ❌ Limited       | ✅ Traditional | ✅ Internal     | ✅ OAuth 2.0         | 2nd          | Competent but no Sieve support          |
| ProtonMail | ✅ Text-based  | ✅ Sieve-based   | ❌ Limited     | ✅ Internal     | ✅ OAuth 2.0         | 3rd          | Privacy-focused, good Sieve support     |
| MXroute    | ❌ Basic GUI   | ❌ Limited       | ❌ Minimal     | ❌ None         | ❌ Basic auth        | 4th          | Basic rules, technical setup required   |
| Namecheap  | ❌ Basic GUI   | ❌ None          | ❌ Minimal     | ❌ None         | ❌ No OAuth 2.0      | 5th          | Limited rule capabilities               |
| AT&T       | ❌ Poor GUI    | ❌ None          | ❌ Broken      | ❌ None         | ❌ Legacy auth       | 6th          | Broken authentication, poor rules       |

#### Hosting Providers - Spam

| Vendor     | Mail.app Rules  | Server-side Rules | Supports Sieve          | Overall Rank | Notes                                             |
|------------|-----------------|-------------------|-------------------------|--------------|---------------------------------------------------|
| Fastmail   | ✅ Full support | ✅ Advanced       | ✅ Full RFC 5228        | 1st          | Best spam filtering, modern dual-interface editor |
| Zoho Mail  | ✅ Full support | ✅ Basic          | ❌ Traditional GUI only | 2nd          | Competent filtering, no Sieve support             |
| ProtonMail | ✅ Full support | ✅ Advanced       | ✅ Sieve-based          | 3rd          | Privacy-focused, good filtering                   |
| MXroute    | ✅ Full support | ✅ Basic          | ❌ Limited              | 4th          | Basic spam protection, technical setup            |
| Namecheap  | ✅ Full support | ❌ Minimal        | ❌ No Sieve             | 5th          | Basic filtering, no OAuth 2.0                     |
| AT&T       | ✅ Limited      | ❌ Poor           | ❌ No Sieve             | 6th          | Degraded service, authentication issues           |

#### MUA Features

| Feature                      | Spark        | Airmail         | Thunderbird    | Outlook      | Canary Mail  | Mimestream   | Postbox      | Mail.app     |
|------------------------------|--------------|-----------------|----------------|--------------|--------------|--------------|--------------|--------------|
| **Base Features**            |              |                 |                |              |              |              |              |              |
| OAuth 2.0 Support            | ✅ Full      | ✅ Full         | ✅ Full        | ✅ Full      | ✅ Full      | ✅ Full      | ✅ Full      | ❌ Limited   |
| IMAP/SMTP Support            | ✅ Full      | ✅ Full         | ✅ Full        | ✅ Full      | ✅ Full      | ✅ Full      | ✅ Full      | ✅ Full      |
| Custom Domain Support        | ✅ Yes       | ✅ Yes          | ✅ Yes         | ✅ Yes       | ✅ Yes       | ✅ Yes       | ✅ Yes       | ✅ Yes       |
| Mobile Apps                  | ✅ Excellent | ✅ Good         | ❌ Limited     | ✅ Excellent | ✅ Good      | ❌ Limited   | ❌ Limited   | ✅ Good      |
| **Critical Differentiators** |              |                 |                |              |              |              |              |              |
| Sieve Rule Support           | ✅ Full      | ✅ Full         | ✅ Full        | ❌ No        | ❌ No        | ❌ No        | ❌ No        | ❌ No        |
| Modern Rule Interface        | ✅ Dual-pane | ✅ Customizable | ✅ Traditional | ❌ Basic GUI | ❌ Basic GUI | ❌ Basic GUI | ❌ Basic GUI | ❌ Basic GUI |
| Spam Filtering               | ✅ Advanced  | ✅ Good         | ✅ Basic       | ✅ Good      | ✅ Good      | ✅ Basic     | ✅ Basic     | ❌ Poor      |
| Version Control              | ✅ Internal  | ✅ Internal     | ✅ Internal    | ❌ None      | ❌ None      | ❌ None      | ❌ None      | ❌ None      |
| **Productivity Features**    |              |                 |                |              |              |              |              |              |
| Calendar Integration         | ✅ Yes       | ✅ Yes          | ✅ Yes         | ✅ Yes       | ❌ No        | ❌ No        | ❌ No        | ❌ No        |
| Contact Sync                 | ✅ Yes       | ✅ Yes          | ✅ Yes         | ✅ Yes       | ❌ No        | ❌ No        | ❌ No        | ❌ No        |
| Search Capabilities          | ✅ Advanced  | ✅ Good         | ✅ Good        | ✅ Good      | ✅ Good      | ✅ Basic     | ✅ Good      | ✅ Basic     |
| **Cost & Ecosystem**         |              |                 |                |              |              |              |              |              |
| Cost                         | Free/Paid    | $5/once         | Free           | Free         | $20/year     | $50/year     | $40/once     | Free         |
| Ecosystem Lock-in            | ❌ None      | ❌ None         | ❌ None        | ✅ Microsoft | ❌ None      | ✅ Gmail     | ❌ None      | ✅ Apple     |
| **Overall Assessment**       |              |                 |                |              |              |              |              |              |
| Modern Tools                 | ✅ Best      | ✅ Good         | ✅ Competent   | ❌ Limited   | ❌ Limited   | ❌ Limited   | ❌ Limited   | ❌ Poor      |
| Authentication               | ✅ Excellent | ✅ Excellent    | ✅ Excellent   | ✅ Good      | ✅ Good      | ✅ Good      | ✅ Good      | ❌ Poor      |
| **Platform Support**         |              |                 |                |              |              |              |              |              |
| macOS                        | ✅ Yes       | ✅ Yes          | ✅ Yes         | ✅ Yes       | ✅ Yes       | ✅ Yes       | ✅ Yes       | ✅ Yes       |
| iOS                          | ✅ Yes       | ✅ Yes          | ❌ No          | ✅ Yes       | ❌ No        | ❌ No        | ❌ No        | ✅ Yes       |
| Chrome                       | ❌ No        | ❌ No           | ❌ No          | ❌ No        | ❌ No        | ❌ No        | ❌ No        | ❌ No        |
| Safari                       | ❌ No        | ❌ No           | ❌ No          | ❌ No        | ❌ No        | ❌ No        | ❌ No        | ❌ No        |
| Firefox                      | ❌ No        | ❌ No           | ❌ No          | ❌ No        | ❌ No        | ❌ No        | ❌ No        | ❌ No        |


#### Hosting Providers - MUA Compatability

Features

| MUA (Mail User Agent) | OAuth 2.0  | Sieve Support | Rule Interface              | Spam Filtering | Mobile Sync  | Cost      | Overall Rank | Notes                                              |
|-----------------------|------------|---------------|-----------------------------|----------------|--------------|-----------|--------------|----------------------------------------------------|
| Spark                 | ✅ Yes     | ✅ Yes        | ✅ Modern dual-interface    | ✅ Advanced    | ✅ Excellent | Free/Paid | 1st          | Best modern interface, excellent OAuth 2.0 support |
| Airmail               | ✅ Yes     | ✅ Yes        | ✅ Highly customizable      | ✅ Good        | ✅ Good      | $5        | 2nd          | Very customizable, good rule system                |
| Thunderbird           | ✅ Yes     | ✅ Yes        | ✅ Traditional but powerful | ✅ Basic       | ✅ Limited   | Free      | 3rd          | Open source, full feature set, dated UI            |
| Outlook               | ✅ Yes     | ❌ No         | ✅ Traditional GUI          | ✅ Good        | ✅ Excellent | Free      | 4th          | Microsoft ecosystem, good mobile sync              |
| Canary Mail           | ✅ Yes     | ❌ No         | ✅ Modern interface         | ✅ Good        | ✅ Good      | $20/year  | 5th          | Native macOS, privacy-focused                      |
| Mimestream            | ✅ Yes     | ❌ No         | ✅ Modern interface         | ✅ Basic       | ❌ Limited   | $50/year  | 6th          | Gmail-focused, native macOS                        |
| Postbox               | ✅ Yes     | ❌ No         | ✅ Traditional GUI          | ✅ Basic       | ❌ Limited   | $40       | 7th          | Thunderbird-based, enhanced features               |
| Mail.app              | ❌ Limited | ❌ No         | ❌ Basic GUI only           | ❌ Poor        | ✅ Good      | Free      | 8th          | Apple ecosystem, legacy authentication issues      |

Compatability Matrix

| MUA / MTA       | Fastmail             | Zoho Mail            | ProtonMail           | MXroute            | Namecheap          | AT&T                  |
|-----------------|----------------------|----------------------|----------------------|--------------------|--------------------|-----------------------|
| **Spark**       | ✅ Full              | ✅ Full              | ✅ Full              | ❌ Basic auth only | ❌ Basic auth only | ❌ Legacy auth issues |
| **Airmail**     | ✅ Full              | ✅ Full              | ✅ Full              | ❌ Basic auth only | ❌ Basic auth only | ❌ Legacy auth issues |
| **Thunderbird** | ✅ Full              | ✅ Full              | ✅ Full              | ✅ Full            | ✅ Full            | ❌ Legacy auth issues |
| **Outlook**     | ✅ Full              | ✅ Full              | ✅ Full              | ✅ Full            | ✅ Full            | ❌ Legacy auth issues |
| **Canary Mail** | ✅ Full              | ✅ Full              | ✅ Full              | ❌ Basic auth only | ❌ Basic auth only | ❌ Legacy auth issues |
| **Mimestream**  | ✅ Full              | ✅ Full              | ✅ Full              | ❌ Basic auth only | ❌ Basic auth only | ❌ Legacy auth issues |
| **Postbox**     | ✅ Full              | ✅ Full              | ✅ Full              | ✅ Full            | ✅ Full            | ❌ Legacy auth issues |
| **Mail.app**    | ❌ Limited OAuth 2.0 | ❌ Limited OAuth 2.0 | ❌ Limited OAuth 2.0 | ❌ Basic auth only | ❌ Basic auth only | ❌ Legacy auth issues |

**Compatibility Notes:**
- **✅ Full:** OAuth 2.0 support, modern authentication, all features work
- **❌ Basic auth only:** Traditional username/password, may have authentication issues
- **❌ Limited OAuth 2.0:** Partial OAuth 2.0 support, some features may not work
- **❌ Legacy auth issues:** AT&T's broken authentication system

**Bottom Line:**
Modern email providers (Fastmail, Zoho, ProtonMail) work well with modern email clients (Spark, Airmail, Thunderbird, Outlook). Legacy providers (MXroute, Namecheap, AT&T) have compatibility issues with modern clients. Mail.app has limited compatibility even with modern providers due to Apple's OAuth 2.0 implementation.

## Next Steps

1. Select a domain name -> RunningWolf.net
2. Select a domain name registrar -> ???
3. Select an email host -> ???
4. Decide **migration option** for your 25 years of mail.
5. Lay out **transition steps** so @att.net forwards during a clean cutover.
