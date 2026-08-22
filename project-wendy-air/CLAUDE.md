# CLAUDE.md

Guidance for working with project-wendy-air.

## Project Overview

Replacement MacBook Air (M3, 2024) for wendy-pro (water damaged, 2026-08). Simplified setup applying lessons from [project-michael-air](../project-michael-air/).

## File Guide

| File                                       | Purpose                                         | Status       |
|--------------------------------------------|-------------------------------------------------|--------------|
| [README.md](README.md)                     | Quick status, hardware specs                    | Current      |
| [setup.md](setup.md)                       | Migration issues, setup checklist, TODO section | Current      |
| [machine_purchase.md](machine_purchase.md) | M1/M2/M3 spec comparison, michael-air reference | Reference    |
| [x86_64-audit.sh](x86_64-audit.sh)         | Reusable Intel binary audit script              | Ready to use |
| [tmutil_analysis](tmutil_analysis)         | Reusable TM exclusion audit script              | Ready to use |
| [CLAUDE.md](CLAUDE.md)                     | This file                                       | Current      |

## Workflow

### Setup Checklist

See [setup.md](setup.md) for detailed TODO items marked with status (pending, in-progress, complete).

### Common Commands

**Run Intel binary audit:**

```bash
./x86_64-audit.sh  # Generates x86_64-audit.log
```

**Check Time Machine exclusions:**

```bash
./tmutil_analysis
```

## Related

- **[project-michael-air](../project-michael-air/)** -- Template and lessons learned
- **[machine_purchase.md](machine_purchase.md)** -- Purchasing guidance and spec recommendations
- **[wolf-soho](../)** -- Main infrastructure repo
