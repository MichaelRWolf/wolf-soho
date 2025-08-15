# Data Migration Plan

## Data Migration Options (25+ years of mail)

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

## Step 1: Data Assessment

- **Estimate total size** of mail for each account:
  - <michaelrwolf@att.net>
  - <wendyrwolf@att.net>  
  - <michaelrunningwolf@att.net>
  - <wendyrunningwolf@att.net>
  - <mbalenger@att.net>

- **Work backwards from now** to estimate storage needs:
  - Previous 6 months
  - Previous 1 year
  - Previous 2 years
  - Previous 3 years
  - Previous 5 years
  - Previous 10 years
  - Forever (complete archive)

## Step 2: Migration Strategy Decision

- **Decide migration strategy** based on:
  - Size of migration (full vs. partial vs. archive)
  - Cost of storage for migrated data
  - Likelihood of using older data
  - Strategy for storing unmigrated data
- **Consider factors:**
  - Storage costs at Fastmail ($3-5/month for 2-25GB)
  - Local storage costs for archives
  - Search frequency of historical data
  - Legal/regulatory retention requirements

## Step 3: Technical Preparation

- **Test Spark with AT&T** (if login works) to get familiar with new MUA
- **Set up Fastmail account** with RunningWolf.net domain
- **Configure DNS records** for email routing
- **Test Fastmail + Spark combination** with new domain
- **Create email aliases** for all existing AT&T addresses

## Step 4: Data Migration Execution

- **Export AT&T data** using IMAP tools or AT&T's export features
- **Import to Fastmail** using their migration tools
- **Verify data integrity** and folder structure
- **Test search functionality** for migrated data
- **Set up forwarding** from AT&T to new addresses

## Step 5: Transition Management

- **Gradual cutover** - forward AT&T emails to new addresses
- **Update critical accounts** (banks, utilities, etc.) to new email
- **Monitor for missed emails** during transition period
- **Keep AT&T account active** for 3-6 months as backup
- **Archive AT&T data** locally before closing account

## Step 6: Post-Migration Cleanup

- **Set up Sieve rules** in Fastmail for email organization
- **Configure Spark** with optimal settings for new workflow
- **Train spam filters** with your email patterns
- **Document new email setup** for future reference
- **Close AT&T account** after confirming no missed emails

## Risk Mitigation

- **Backup strategy** for all data before migration
- **Rollback plan** if issues arise during migration
- **Communication plan** for family members affected by email changes
- **Timeline buffer** for unexpected technical issues
