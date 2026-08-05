# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**project-macbook-x2-reshuffle** documents hardware recovery strategy for two MacBook machines following water damage incidents (wendy-pro: 2026-08-03, michael-pro: 2026-06-18). This is a decision-analysis project: no build system, no tests, no application code -- purely Markdown documentation with quantitative hardware comparison matrices.

**Key characteristic:** The goal is to recommend optimal upgrade paths (used M-series machines, or interim machine reuse) by cost, timeline, and risk. All data is in Markdown tables for easy comparison.

## Repository Structure

### Documentation Files

- **notes.md** -- Executive summary: problem statement, strategy options (A/B/C/D), recommendation, timeline, next steps
- **michael-options.md** -- Detailed machine comparison matrix for Michael's workflow (Claude Code + git operations); five machine options rated across 12 dimensions
- **wendy-options.md** -- Detailed machine comparison matrix for Wendy's workflow (SaaS-first browser user); machine options vs. interim wolf-air analysis

### Hardware Decision Matrices

Each `*-options.md` file contains identical structure:

1. Workload constraints (what matters for that user)
2. Comparison matrix for 4-5 candidate machines (dimensions: compatibility, cost, lifespan, risk)
3. Recommendation with decision paths and timeline
4. Backup information (NAS restore dates, data loss assessment)

### Context Files (Parent Repo)

Decision matrices reference external files from **wolf-soho** root:

- **CONTEXT.md** -- Canonical device registry (michael-pro, wendy-pro, wolf-air, beryl, etc.)
- **equipment_computing.md** -- Detailed hardware specs for all machines

## Constraints and Gotchas

### Constraint 1: Monterey EOL (Mid-2026)

- wolf-air (2015 Intel) is capped at macOS Monterey 12.7.6; cannot upgrade
- Monterey reaches EOL mid-2026 (~6 months from 2026-08-05)
- Any machine stuck on Monterey after EOL has no security patches
- Michael can defer upgrade to mid-2026 if budget is tight; Wendy must move off wolf-air by then

### Constraint 2: NAS Backup Freshness

- Both wendy-pro and michael-pro have Time Machine backups dated **2026-06-27** (38 days / ~5.5 weeks old)
- Data loss is minimal: SaaS data lives in cloud; code repos are remote (GitHub)
- Backup is sufficient for restore, though recent files (e.g., last 3 weeks' work) are not backed up
- If critical data is missing, send wendy-pro SSD to recovery lab (~$600); otherwise skip

### Constraint 3: Budget Sensitivity

- Both users are cost-sensitive; project recommends **used/refurbished M-series over expensive repairs**
- Total cost estimate: $500-$900 for both users (vs. $400-$700 for repair-only path)
- wolf-air reuse eliminates one machine cost; Michael can defer upgrade to mid-2026 if cash flow is tight

## Common Tasks

### Update Hardware Comparison

1. Add new candidate machine to the `*-options.md` file (new row in the comparison matrix)
2. Rate across all dimensions (Claude Code compatibility, cost, lifespan, risk, etc.)
3. Ensure consistency with existing rows (same rating scale: ✅ EXCELLENT / ⚠️ ACCEPTABLE / ❌ etc.)
4. Run markdownlint to align table columns

### Add Decision or Timeline

1. Edit **notes.md** (main decision log)
2. Add new option under "## Options Summary" or update "## Timeline"
3. Link to relevant `*-options.md` analysis

### Reference External Canonical Data

- Always check **wolf-soho/CONTEXT.md** for canonical device names (michael-pro, wendy-pro, wolf-air, beryl)
- Refer to **wolf-soho/equipment_computing.md** for detailed hardware specs
- Do NOT invent device names or aliases; use canonical names from CONTEXT.md

## Markdown Conventions

- **Line length:** No hard limit (uses soft-wrap; emacs M-q unfills)
- **Table alignment:** markdown-table-formatter auto-aligns on commit
- **No smart quotes:** texthooks normalize ligatures/smartquotes/dashes on commit

## Structure for Decision Matrices

### Workload Constraints Table

Column headers: Factor | Impact | Notes

Rows: Each workload dimension (e.g., Claude Code, git operations, Homebrew, battery life) with visual indicator (e.g., MEDIUM, LOW) and brief explanation.

### Machine Options Table

Column headers: Dimension | Rating | Assessment

Rows: Each hardware/OS dimension rated with emoji (✅ EXCELLENT / ⚠️ ACCEPTABLE / ❌ NOT SUITABLE) and explanation.

Example:

```markdown
| Dimension                     | Rating     | Assessment                    |
|-------------------------------|------------|-------------------------------|
| **Claude Code compatibility** | ✅ WORKS    | Confirmed running on Monterey |
| **macOS updates**             | ⚠️ CAUTION | Monterey EOL mid-2026         |
```

### Decision Paths

Use ordered lists (1. 2. 3.) with **Timeline:** and **Rationale:** subheadings. Include data loss assessment and success probability.

## Key Data Points (Static, Updated 2026-08-04)

- **wendy-pro:** M2 MacBook Pro (2022), water damage 2026-08-03, power management failure (boot stalls, GPU glitch)
- **michael-pro:** 2020 Intel MacBook Pro, water damage 2026-06-18, disassembled but not reassembled
- **wolf-air:** 2015 MacBook Air (Intel), Monterey 12.7.6 (capped), currently running Claude Code successfully
- **NAS backup date:** 2026-06-27 (5.5 weeks old)
- **Monterey EOL:** Mid-2026 (~6 months from current date)

## When to Ask About

- **Device specs or names:** Check wolf-soho/CONTEXT.md first for canonical registry
- **Hardware compatibility:** Consult equipment_computing.md for detailed specs
- **Timeline or cost reassessment:** Edit notes.md or corresponding `*-options.md` file with new data
- **Decision recommendation:** Ensure recommendation aligns with cost, timeline, and risk tradeoffs in the matrices

## No Build, No Tests

This project has **no build system, no tests, no CI/CD**. Quality is enforced through:

- Markdown lint (table alignment, prose formatting)
- Manual review of decision matrices for consistency
- Verification that numbers (cost, timeline, success probability) match across files

Do NOT add build scripts, tests, or CI pipelines unless explicitly requested.

---

## Shopping File Naming and Structure (eBay Hunt Snapshots)

### File Organization

**@shopping.md** = Single source of truth for active top contenders. Summary of the best options currently under consideration, with strikethrough used to mark items no longer viable (never delete rows).

**shopping-YYYY-MM-DDTHH:MM.md** = Timestamped snapshots of eBay search results. Each file captures a specific search/view on a given date+time. Useful for tracking how market inventory evolves over hours/days.

### Table Format (All Files)

All shopping files (both @shopping.md and snapshot files) use identical table format:

```markdown
| #     | Offering          | CPU + Model + Screen | RAM | Disk | Price | OS/EOL        | Video    | Batt | MDM | Cond        | Status       |
|-------|-------------------|----------------------|-----|------|-------|---------------|----------|------|-----|-------------|--------------|
| 0     | wolf-air          | i5 1.8 dual          | 8   | 128  |       | Monterey/2026 | 1440×900 | 630  | No  | Good        | Interim      |
| 3     | #3                | M3 Air 13            | 16  | ???  |       | Sonoma/2028   | 1080p+   | ???  | ??? | ???         | Out of stock |
| ~~1~~ | ~~#1 (archived)~~ | M2 Air 13            | 16  | 512  | 615   | Sonoma/2028   | 1080p+   | ???  | ??? | eBay Refurb | Superseded   |
```

### Offering ID (Cross-Snapshot Numbering)

Numbers increment **across all snapshot files** to create a persistent offering ID. This allows referencing the same listing consistently, even as it appears in different snapshots or time periods.

**Example:** #43, #44, #45 are unique IDs that stay the same whether you find them in shopping.md or shopping-2026-08-05T14:55.md.

### Strikethrough (No Deletion)

When an offering is no longer viable:

- ~~Strikethrough the entire row~~ (never delete)
- Update the Status column (e.g., "Sold out", "Superseded", "Seller unresponsive")
- Add brief explanation in parentheses (e.g., `~~#1 (archived)~~` or `~~#2 (unavailable)~~`)

This preserves history and context for future reference.

### Sub-Headings (Detailed Offering Info)

Each offering with a summary row also has a detailed sub-heading section:

```markdown
### #43 --- gadgetpickup M3 Open Box 256GB (🟢 AVAILABLE NOW)

**Status:** Active listing; awaiting seller response on MagSafe 3 adapter

- **Link:** [eBay Listing #307108920696](https://www.ebay.com/itm/307108920696)
- **Seller:** gadgetpickup (99.9% positive, 17.4K ratings)
- **Price:** $749.99
- **Machine:** Apple MacBook Air (13-inch, M3, 2024 model A3113), 16GB RAM, 256GB SSD, Space Gray
- **Condition:** Open Box (brand new, box opened, never used)
- ... [more details]
```

**URL Preservation:** Once a URL is captured (from eBay or other source), **preserve it in future edits**. This allows navigating back to the exact listing for verification, tracking price changes, or confirming availability.

If URL is not available (e.g., text/image scrape of search results without direct link), note "TBD" or omit the Link field. Once a URL is found later, add it and preserve it.

### Snapshot Usage

Create a new snapshot file when:

- Hunting a specific segment (e.g., "M3 16GB on eBay," "refurbished M2 options")
- Capturing market inventory at a specific time (useful for tracking price trends, stock rotation)
- Organizing search results into the common table format

Snapshots complement @shopping.md; they don't replace it. The main file stays focused on top contenders.
