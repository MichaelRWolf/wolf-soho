# [CLAUDE.md](CLAUDE.md)

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Directory Is

Document set for the AT&T billing dispute (account details and history in [README.md](README.md)). It is not a software project: there are no builds, test suites, or linters specific to this directory. The parent repo (`/Users/michael/repos/wolf-soho`) root [CLAUDE.md](CLAUDE.md) governs git hooks, shellcheck, and markdownlint for committed files.

## Files and Roles

- **[README.md](README.md)** - Source of truth for account facts, timeline, and next actions. Update it when facts change.
- **TODO.md** - Pre-submission checklist and evidence gaps. Keep it in sync with [README.md](README.md)'s "Next Actions".
- **[dispute_letter_final.md](dispute_letter_final.md)** - Letter to submit via att.com/dispute. Edit only after Wendy's review.
- **[dispute_letter_outline.md](dispute_letter_outline.md)** - Earlier outline the final letter was built from.
- **[PLAN_dispute.md](PLAN_dispute.md)** - Strategy, escalation path, and negotiation positions.
- **[billing_data.jsonl](billing_data.jsonl)** - One JSON object per bill (`month`, `total_due`, per-line `*_plan`/`*_base`/`*_total`, `notes`). Structured source for the summary table.
- **[billing_summary_table.md](billing_summary_table.md)** - Month-by-month table derived from [billing_data.jsonl](billing_data.jsonl).
- **[analysis_august_2026_bill.md](analysis_august_2026_bill.md)** - Line-item breakdown of the August 2026 bill.
- **[customer_profile_and_evidence.md](customer_profile_and_evidence.md)** - Evidence summary and customer usage profile.
- **[call_log_2026-10-13.md](call_log_2026-10-13.md)** - Call notes from Oct 13, 2026 (611 bot, John, Eliza, Danielle).

## Working Conventions

- When changing a number, update every file that cites it. Billing totals appear in [README.md](README.md), [billing_summary_table.md](billing_summary_table.md), [billing_data.jsonl](billing_data.jsonl), and the dispute letter. Check with `grep -rn "<old value>" .` before editing.
- Do not add a file that lacks a source document or a note on where its figures came from.
- Mark unverified claims as unverified. [README.md](README.md) flags the IMEA misclassification as hearsay from the Oct 8 call until AT&T records confirm it.
- Keep prose paragraphs as single long lines (no hard wraps). Tables and lists keep their line breaks.
- Use the same identifiers as existing docs; do not retype account or phone numbers from memory.
- Planned subdirectories (`bills/`, `transcripts/`, `receipts/`, `letters/`) from [README.md](README.md) do not exist yet. Create them only when adding files for them.

## Known Inconsistencies

- [README.md](README.md) and TODO.md point to [`PLAN_dispute.md`](PLAN_dispute.md) and `DISPUTE_LETTER_OUTLINE.md`. The actual filenames are lowercase.
- Estimated overcharge differs between documents: [README.md](README.md) says $750-1000+, [PLAN_dispute.md](PLAN_dispute.md) says $450-825 in one section and $2,000-2,500 in another. Reconcile before the letter cites a total.
- [dispute_letter_final.md](dispute_letter_final.md) header says "Submitted: 2026-10-13", but its status line and TODO.md say not yet submitted.
