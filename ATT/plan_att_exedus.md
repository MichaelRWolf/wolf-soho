# plan_att_exedus.md

## Past 10--20 Years --- Problems with @att.net

1.  **Zero support**
    -   Since AT&T made it free, they've given exactly \$0 worth of
        service and support.\
2.  **Account tied to ISP**
    -   Locked to AT&T/Yahoo backend whims with no provider choice.\
3.  **Random service breaks**
    -   Working on one device, failing on others, with no fix path
        except waiting or changing passwords.\
4.  **Password-change cascades**
    -   Change → update everywhere → sometimes change again within
        hours.\
5.  **Opaque operations**
    -   No service status, no logs, no admin control.\
6.  **No roadmap or improvement**
    -   Treated as a cost sink, not a real product.

## Next 10--20 Years --- Vision for Mail Hosting

1.  **Provider independence**
    -   Email address not tied to an ISP or big ecosystem;
        **RunningWolf.net** becomes the permanent identity.\
2.  **Professional-grade reliability**
    -   Hosted by experts (IaaS-level managed service), not self-run
        hardware.\
3.  **Standards-compliant access**
    -   Smooth IMAP/SMTP for Mail.app, no lockouts or forced webmail.\
4.  **Transition safety net**
    -   @att.net forwards to the new address during a controlled
        migration.\
5.  **Security without chaos**
    -   MFA, app passwords, passkeys that don't throw every device
        offline.\
6.  **Archival and export**
    -   Full data control; the host provides reliable export tools to
        leave at any time.\
7.  **Longevity**
    -   Service likely to exist and stay standards-compliant into the
        2040s.

## Data Migration Options (25+ years of mail)

  ---------------------------------------------------------------------------------
  Option        Description         Pros         Cons         Typical Cost
  ------------- ------------------- ------------ ------------ ---------------------
  **Full        Copy every          All history  Larger       \$0--\$100 one-time
  migration**   message + folder    searchable   mailbox      if DIY; \$200--\$500
                into new provider   in one place cost; more   if hiring migration
                                                 time to      service
                                                 transfer     

  **Partial     Move only recent    Lower        Old mail     \$0--\$50 if DIY
  migration**   mail (e.g., last    storage      stays        
                1--3 years)         cost; faster separate,    
                                    migration    requires     
                                                 legacy       
                                                 access       

  **Archive +   Export old mail to  No ongoing   Searching    \$0--\$50 for storage
  clean start** .mbox and store     hosting cost old mail is  
                offline; new inbox  for old      clunkier;    
                starts empty        mail;        requires     
                                    fastest new  opening      
                                    setup        archives     
                                                 separately   
  ---------------------------------------------------------------------------------

## Clarifications

-   **Self-host vs IaaS**: Self-host = your server, your electric bill,
    your patching headaches → ruled out. IaaS email hosting = paying a
    provider to run it for you on their hardware.
-   **Decoupling from iCloud/Gmail/Outlook.com**: You can still read
    mail in any client, but the mailbox lives on RunningWolf.net's
    provider.
-   **Archival strategy**: Decide if your email provider is your
    long-term archive or if you keep historical archives offline.

## Next Steps

1.  Pick a **RunningWolf.net** registrar + email host shortlist.
2.  Decide **migration option** for your 25 years of mail.
3.  Lay out **transition steps** so @att.net forwards during a clean
    cutover.
