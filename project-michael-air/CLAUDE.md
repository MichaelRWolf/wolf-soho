# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**project-michael-air** tracks the purchase, setup, and configuration of a new MacBook Air (M3, 13-inch, 2024) to replace michael-pro. This is primarily a project-tracking repository with documentation, not a software project.

**Key files:**

- `notes.md` -- Purchase details, specs, and progress checklist

**Related projects:**

- `project-macbook-x2-reshuffle` -- Broader reshuffling/reallocation of multiple MacBooks
- `wolf-soho` (global) -- Main SOHO infrastructure; michael-pro status tracked in [project_michael_pro_status.md](../wolf-soho/project_michael_pro_status.md)

## Common Tasks

### Update Project Status

Edit the progress checklist in `notes.md` under "Project Progress". Keep items as discrete, actionable steps.

### Add New Phase or Section

Add a new `##` heading and structured list (no excessive prose). Example:

```markdown
## Setup Steps

- [ ] Install Homebrew
- [ ] Clone dotfiles repo
- [ ] Run portable-profile install
```

### Document Issues or Findings

If blocking issues arise (hardware defects, shipping delays, etc.), add them as notes directly in `notes.md` or create a dated incident file if required by the broader wolf-soho workflow.

## Markdown Conventions

Follow the global conventions from [~/.claude/CLAUDE.md](https://github.com/anthropics/claude-code):

- **Line wrapping:** No hard newlines in prose (emacs soft-wrap handles display)
- **Structure:** Use `##` / `###` headings and numbered/bulleted lists for clarity
- **No org files** -- Markdown only

## Context

This machine will replace michael-pro (currently disassembled; logic board extraction paused 2026-06-23). Prioritize setup efficiency to restore full development environment as quickly as possible once the unit arrives.
