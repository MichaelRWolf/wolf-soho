# Confluence Cloud Free Site Deletion  
## What Happened and What Support Confirmed

This document records a real experience involving the suspension and permanent deletion of a long-standing **Confluence Cloud Free** site in late 2025.

It exists for one reason: **to help other users understand data-loss risk earlier than I did**, and to document what Atlassian support confirmed after the deletion occurred.

I do not expect my data to be recovered.  
My goal is simpler — that fewer people lose theirs.

Everything below is based on written support responses, case records, and observed behavior.

---

## Quick Summary (Key Findings)

- A long-standing Confluence Cloud Free site was deactivated and permanently deleted due to inactivity.
  
- The day after receiving a message indicating that accounts

- Subscription was cancelled 42 days after most recent login.
- Data was deleted after a 14-day soft-deletion window.
- Customer was unable to login 56 days after most recent login.
- 
logged in 56(?) days after most recent login to find subscription cancelled.

after 42 days of activity.
- Data was deleted after
- Data was deleted after a 14-day soft-deletion window, but before 
- Customer login 56(?) days after most recent login was beyond the 14-day soft-deletion window.
- Prior written guidance stated a **120-day inactivity window**; support later confirmed the window had been reduced to **~40 days**.
- This change was not discoverable in public documentation at the time of deletion.
- Multiple Atlassian teams were engaged over several weeks.
- All teams ultimately confirmed that **no recovery path exists** once deletion completes.

This document is shared so others can take preventative action sooner.

---

## What This Means for Other Users (Practical Warnings)

- **Free ≠ safe**
- Inactivity windows may change
- “Login counts as activity” depends on backend classification
- Email-only warnings are risky in a phishing-heavy environment
- **Export early, export often**

---

## Timeline of Events

### September 29, 2025
An Atlassian Customer Advocate, responding to a Billing & Licensing support request, stated in writing:

> “Confluence on a Free plan will be deactivated after 120 days of inactivity. To prevent your site from being deactivated, just log in and view any Confluence page — that’ll count as activity and reset the 120-day clock.”

### September 30, 2025
I used my Confluence site extensively. Atlassian later confirmed that this activity occurred.

### November 30, 2025
I was informed by a Billing & Licensing team member that:

> “Your Confluence subscription… was cancelled on November 13, 2025, due to inactivity.”

This meant that **just 44 days after confirmed use**, the site had been deactivated — and, following a 14-day soft-deletion window, permanently deleted due to “inactivity.”

### December 2025
For just over a month, I engaged in a sustained effort to understand what had happened and whether recovery was possible, involving multiple Atlassian teams.

### December 30, 2025
Atlassian Cloud Support informed me:

> “The inactivity period was updated from 120 days to 40 days. Unfortunately, there are no options to recover the data.”

At no point prior to deletion was a **40-day inactivity threshold** clearly communicated in a way that allowed me to make an informed decision about safeguarding my data.

### January 13, 2026
As of this date, I was unable to locate any publicly accessible Atlassian documentation that describes a 40-day inactivity threshold for Confluence Free plan sites. Public documentation references only deactivation after a general period of inactivity, without specifying a numeric value.

---

## FAQ

### FAQ #1: What support channels were involved?

Departments interfaced with:

- Chatbot → human escalation path
- Automation / Jira Service Desk
- Customer Advocate (Billing & Licensing)
- GDPR / Data Subject Access (DSAR)
- Confluence Cloud Support
- Deactivation / Inactivity Service (internal)
- Internal deactivation-service review (via Cloud Support)

**Case / ticket numbers**
- DATA-49352 (DSAR)
- DATA-49608 (follow-up, cancelled)
- JST-1229029 (technical review)

---

### FAQ #2: Were warning emails sent?

Yes — **three emails were sent**, and I missed them.

This is not a case of “no notice.”  
That part is mine.

However, here is the nuance.

#### How a reasonable person can lose data under these conditions

- I had been told weeks earlier, in writing, that inactivity meant **120 days**.
- The emails resembled years of prior routine SaaS notices.
- The safety margin had silently collapsed from months to weeks.
- Once deletion completed, **no recovery was possible** — even through support.

By the time I understood this, the data was already (allegedly) gone.

#### Owning my part

Could I have caught the emails sooner? Yes.  
Could I have been more vigilant? Also yes.

But:
- My expectations were shaped by years of prior experience.
- Email overload and phishing have changed how people triage attention.
- Nothing in the messages unmistakably signaled: **“This is different — act now or lose everything.”**

---

### FAQ #3: Why am I sharing this?

I’m not sharing this to complain or assign blame.

I’m sharing it to say something plainly:

> **If you use Confluence — especially on a Free plan — proactively export or back up your data.**

Do not assume time buffers, recovery options, or continuity with prior guidance.

---

## Why This Matters

Life does not happen in neat, low-noise windows.

Births.  
Deaths.  
Illness.  
Injury.  
Moves.  
Multiple responsibilities.

Systems that quietly collapse safety margins — from months to weeks — without a clear, durable signal are not designed for humans living real lives.

---

## About the Experience

The Confluence product itself was genuinely useful.

What followed was deeply disappointing: a month-long effort involving multiple teams and dozens of hours of focused attention — after the data was already unrecoverable.

The issue was not individual conduct, but **rules that changed without a clear reference point**.

---

## My Hope in Sharing This

- That others take proactive steps to protect their data.
- That clearer, more actionable safeguards become standard.

---

## Appendix: Scope and Intent

This document reflects one user’s documented experience with Confluence Cloud Free, based on written support responses and case records from December 2025.

### This document **is**:
- A factual record of observed behavior and support-confirmed outcomes
- A practical warning for other users

### This document **is not**:
- A claim of wrongdoing
- Legal advice
- A vendor comparison
- A request for special treatment
