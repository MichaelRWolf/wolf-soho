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

- Namecheap - Competitive pricing, good UI, strong reputation
- Google Domains - Simple interface, integrates well with other Google services
- Cloudflare - Very competitive pricing, excellent security features
- GoDaddy - Well-known, extensive features but more aggressive upselling

### Email Hosting Providers

Recommended providers:

- MXroute - Excellent value, multiple domains allowed, technical setup required
- Fastmail - Great interface, custom domain support, strong privacy focus
- Zoho Mail - Affordable, includes business tools, can be complex to set up
- Microsoft 365 - Full Office suite included, enterprise-grade but costlier
- ProtonMail - End-to-end encryption, privacy focused, premium pricing

#### Important Considerations

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

## Next Steps

1. Select a domain name -> RunningWolf.net
2. Select a domain name registrar -> ???
3. Select an email host -> ???
4. Decide **migration option** for your 25 years of mail.
5. Lay out **transition steps** so @att.net forwards during a clean cutover.
