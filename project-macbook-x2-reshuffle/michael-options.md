# Michael's Machine Options Analysis

**Focus:** Michael's independent + dependent hardware needs. Light development (git, Claude Code); machine type depends on Wendy's adoption plan.

**Key assumption:** Claude Code is cloud-based; minimal local hardware required (4GB RAM minimum, 16GB recommended).

**Decision:** Which machine offers best value for Michael's light development workflow?

---

## Claude Code Clarification

**Important finding:** Claude Code does NOT require local GPU or computation.

- Cloud-based: Anthropic servers run the model inference
- Hardware requirements: 4GB RAM minimum; 16GB recommended for multi-file work
- Supported on macOS 13+ officially; however, **Claude Code 2.1.221 runs successfully on Monterey 12.7.6**
- Michael is currently running Claude Code on wolf-air (confirmed: works in practice)

**Correction:** wolf-air CAN run Claude Code. The Monterey limitation in official docs does not match real-world usage.

---

## Workload Constraints

| Factor                | Impact | Notes                                                                                    |
|-----------------------|--------|------------------------------------------------------------------------------------------|
| **Claude Code**       | MEDIUM | Cloud-based; runs on any modern Mac with macOS 13+. Minimal local load.                  |
| **Git operations**    | LOW    | Clone, push, pull, commit; no CI/CD pipelines. Light CLI usage.                          |
| **Bash scripting**    | LOW    | Writing automation scripts; not compilation-heavy.                                       |
| **Local development** | NONE   | Not building apps; no compilers, heavy frameworks, or databases.                         |
| **Terminal work**     | LOW    | SSH, grep, find, rsync; standard Unix tooling.                                           |
| **Homebrew**          | MEDIUM | Needs to work without warnings/errors for package installs (Intel deprecation is a nag). |
| **NAS backup**        | MEDIUM | Restore from 2026-06-27 Time Machine backup (5+ weeks old; acceptable).                  |

---

## Machine Options Matrix

### Option 1: wolf-air (2015 MacBook Air, Intel Core i5, 8GB RAM)

| Dimension                     | Rating          | Assessment                                                                                                                   |
|-------------------------------|-----------------|------------------------------------------------------------------------------------------------------------------------------|
| **Claude Code compatibility** | ✅ WORKS         | Claude Code 2.1.221 runs successfully on Monterey 12.7.6 (confirmed: Michael using it now).                                  |
| **Git operations**            | ✅ ACCEPTABLE    | Bash + git work fine on Intel; no issues with CLI.                                                                           |
| **Homebrew**                  | ⚠️ ACCEPTABLE   | Intel deprecation warnings are cosmetic; packages install but nag about compatibility. Acceptable as-is; annoying long-term. |
| **Bash scripting**            | ✅ ACCEPTABLE    | Shell scripting works fine; no performance bottleneck.                                                                       |
| **Terminal performance**      | ⚠️ ACCEPTABLE   | Intel dual-core is slower than M-series for parallel operations; acceptable for light scripts.                               |
| **Terminal startup**          | ⚠️ ACCEPTABLE   | Slower shell startup (~2-3 seconds); old hardware. Manageable.                                                               |
| **Battery life**              | ⚠️ ACCEPTABLE   | 11-year-old battery: 3-5 hours typical; needs power adapter for extended sessions.                                           |
| **Thermals**                  | ⚠️ ACCEPTABLE   | Fan spins under load; loud compared to M-series. Acceptable for desk work.                                                   |
| **macOS updates**             | ⚠️ CAUTION      | Stuck at Monterey; EOL mid-2026 (~6 months). No future security patches after that.                                          |
| **Future-proofing**           | ⚠️ INTERIM ONLY | Works now, but Monterey EOL is a ticking clock. Not viable beyond mid-2026 without accepting security risk.                  |
| **Cost**                      | ✅ EXCELLENT     | $0 (already running; no purchase needed).                                                                                    |
| **Overall verdict**           | ⚠️ INTERIM ONLY | **Works now. Acceptable as interim machine through mid-2026. Not suitable as long-term primary (OS EOL).**                   |

**Viable path:** Michael can continue using wolf-air for Claude Code + git work through mid-2026. Plan to upgrade to M3/M4 when Monterey reaches EOL or sooner if security concerns arise.

---

### Option 2: M2 MacBook Air or Pro (2022, 8GB RAM)

| Dimension                     | Rating       | Assessment                                                                  |
|-------------------------------|--------------|-----------------------------------------------------------------------------|
| **Claude Code compatibility** | ✅ EXCELLENT  | Sonoma/Tahoe current; macOS 13+ fully supported. Claude Code runs natively. |
| **Git operations**            | ✅ EXCELLENT  | M2 + git: lightning-fast clone/push/pull; no bottlenecks.                   |
| **Homebrew**                  | ✅ EXCELLENT  | Apple Silicon; no Intel warnings. Clean package installs.                   |
| **Bash scripting**            | ✅ EXCELLENT  | M2 single-thread performance is faster than new Intel; scripting is snappy. |
| **Terminal performance**      | ✅ EXCELLENT  | M2 launch speed <1 second; parallel operations are fast.                    |
| **Terminal startup**          | ✅ EXCELLENT  | <1 second boot to prompt.                                                   |
| **Battery life**              | ✅ EXCELLENT  | 14-18 hours typical; M2 efficiency is solid.                                |
| **Thermals**                  | ✅ EXCELLENT  | M2 runs cool; silent under typical load.                                    |
| **macOS updates**             | ✅ EXCELLENT  | Tahoe current; patches through ~2029.                                       |
| **Future-proofing**           | ✅ GOOD       | Viable through 2027-2028; M2 is aging but not obsolete.                     |
| **Cost**                      | ✅ GOOD       | Used 2022 M2 Air: $400-$600. Affordable.                                    |
| **Avoid shitty 2022 Pro**     | ⚠️ CAUTION   | 2022 M2 Pro had thermal issues (fans loud); Air is fine. Stick with Air.    |
| **Overall verdict**           | ✅ ACCEPTABLE | **Works. Meets all requirements. Older than M3/M4 but cost-effective.**     |

**Trade-off:** M2 is aging; will start feeling behind 2027+, but fine for light development through 2028.

**Success probability:** ~95% (proven chip; 2 years old).

---

### Option 3: M3 MacBook Air (2023, 16GB RAM) ← RECOMMENDED

| Dimension                     | Rating      | Assessment                                                               |
|-------------------------------|-------------|--------------------------------------------------------------------------|
| **Claude Code compatibility** | ✅ EXCELLENT | Tahoe current; macOS support through ~2030. Claude Code runs flawlessly. |
| **Git operations**            | ✅ EXCELLENT | M3 git performance excellent; large repo clones are fast.                |
| **Homebrew**                  | ✅ EXCELLENT | Apple Silicon; zero warnings. Clean installs.                            |
| **Bash scripting**            | ✅ EXCELLENT | M3 efficiency cores handle scripting effortlessly.                       |
| **Terminal performance**      | ✅ EXCELLENT | M3 <1 second startup; parallel operations are smooth.                    |
| **Terminal startup**          | ✅ EXCELLENT | Boot to prompt <10 seconds.                                              |
| **Battery life**              | ✅ EXCELLENT | 15-18 hours typical; M3 efficiency is best-in-class for its era.         |
| **Thermals**                  | ✅ EXCELLENT | M3 silent under all typical loads.                                       |
| **macOS updates**             | ✅ EXCELLENT | Tahoe current; patches through ~2030+.                                   |
| **Future-proofing**           | ✅ EXCELLENT | Viable primary through 2027+; no worries about OS support.               |
| **Cost**                      | ✅ GOOD      | Used 2023 M3 Air 16GB: $500-$700. Sweet spot for value.                  |
| **Avoid shitty models**       | ✅ N/A       | M3 Air is solid; no known issues.                                        |
| **Overall verdict**           | ✅ EXCELLENT | **RECOMMENDED. Best balance for Michael's light development.**           |

**Why M3 over M2:** +$100-$150 gets newer chip, better thermals, more longevity. Worth the premium.

**Success probability:** ~95% (proven chip; ~1 year field history).

---

### Option 4: M4 MacBook Air (2024, 16GB RAM)

| Dimension                     | Rating      | Assessment                                                                                                     |
|-------------------------------|-------------|----------------------------------------------------------------------------------------------------------------|
| **Claude Code compatibility** | ✅ EXCELLENT | Latest macOS; patches through ~2031.                                                                           |
| **Git operations**            | ✅ EXCELLENT | M4 performance is overkill for git; ultrafast.                                                                 |
| **Homebrew**                  | ✅ EXCELLENT | Apple Silicon latest; pristine package support.                                                                |
| **Bash scripting**            | ✅ EXCELLENT | M4 efficiency is overkill; scripts complete instantly.                                                         |
| **Terminal performance**      | ✅ EXCELLENT | M4 <1 second startup; no lag ever.                                                                             |
| **Terminal startup**          | ✅ EXCELLENT | <10 second boot.                                                                                               |
| **Battery life**              | ✅ EXCELLENT | 16-20 hours typical; M4 is peak efficiency.                                                                    |
| **Thermals**                  | ✅ EXCELLENT | M4 thermal efficiency best-in-class.                                                                           |
| **macOS updates**             | ✅ EXCELLENT | Cutting-edge; patches through ~2031+.                                                                          |
| **Future-proofing**           | ✅ EXCELLENT | Future-proofed through 2029+.                                                                                  |
| **Cost**                      | ⚠️ HIGHER   | Used 2024 M4 Air 16GB: $700-$900. Premium over M3.                                                             |
| **Avoid shitty models**       | ✅ N/A       | M4 Air is solid; no known issues.                                                                              |
| **Overall verdict**           | ⚠️ OVERKILL | **OVERKILL for Michael's workload. M3 is already sufficient; M4 premium not justified for git + Claude Code.** |

**When to buy M4:** If future budget allows and Michael wants cutting-edge; skip for now.

**Success probability:** ~95% (latest chip; proven in field).

---

### Option 5: M5 MacBook Air (2025, 16GB RAM)

| Dimension                     | Rating                 | Assessment                                                                 |
|-------------------------------|------------------------|----------------------------------------------------------------------------|
| **Claude Code compatibility** | ✅ EXCELLENT            | Latest macOS; patches through ~2032+.                                      |
| **Git operations**            | ✅ EXCELLENT            | M5 performance is overkill for git; unnecessary premium.                   |
| **Homebrew**                  | ✅ EXCELLENT            | Latest Apple Silicon; perfect support.                                     |
| **Bash scripting**            | ✅ EXCELLENT            | M5 overkill for scripting.                                                 |
| **Terminal performance**      | ✅ EXCELLENT            | M5 <1 second startup.                                                      |
| **Terminal startup**          | ✅ EXCELLENT            | <10 second boot.                                                           |
| **Battery life**              | ✅ EXCELLENT            | 17-21 hours typical; peak efficiency.                                      |
| **Thermals**                  | ✅ EXCELLENT            | M5 best-in-class thermals.                                                 |
| **macOS updates**             | ✅ EXCELLENT            | Latest; longest support window (7+ years).                                 |
| **Future-proofing**           | ✅ EXCELLENT            | Overkill; viable through 2031+.                                            |
| **Cost**                      | ❌ EXPENSIVE            | New 2025 M5 Air: $1,200-$1,400. 2-3x M3 cost.                              |
| **Avoid shitty models**       | ✅ N/A                  | M5 Air is solid.                                                           |
| **Overall verdict**           | ❌ OVERKILL & EXPENSIVE | **NOT RECOMMENDED. M5 is overkill for light development and costs 2x M3.** |

**When to buy M5:** Only if Michael wants bleeding-edge and has budget; skip for now.

---

## Michael's Recommendation Matrix

| Machine                | Cost      | Viability                        | Recommendation                     | Timeline               |
|------------------------|-----------|----------------------------------|------------------------------------|------------------------|
| **wolf-air (interim)** | $0        | Works now; Monterey EOL mid-2026 | ✅ Use now / ⚠️ Upgrade at mid-2026 | Defer upgrade 6 months |
| **M2 Air 8GB+**        | $400-$600 | Acceptable (older chip)          | ⚠️ Optional if budget tight        | N/A                    |
| **M3 Air 16GB**        | $500-$700 | Excellent (primary)              | ✅ RECOMMENDED (upgrade now)        | ASAP                   |
| **M4 Air 16GB**        | $700-$900 | Excellent (overkill)             | ⚠️ Optional upgrade path 2027+     | N/A                    |
| **M5 Air 16GB**        | $1,200+   | Excellent (overkill + expensive) | ❌ Not recommended                  | N/A                    |

---

## Michael's Decision Paths

**Current status:** Claude Code works on wolf-air (Monterey 12.7.6). No immediate blocker.

**Constraint:** Monterey EOL mid-2026 (~6 months away). Plan upgrade before then or accept security patching gap.

### Option 1: Continue on wolf-air Until Mid-2026 (Defer Cost)

**Path:** Use wolf-air as-is; upgrade machine around mid-2026 when Monterey reaches EOL.

**Timeline:**

- **Now through 2026-06:** Continue using wolf-air for Claude Code + git
- **June 2026:** Begin hunting M3/M4 Air
- **July 2026:** Migrate to new machine before Monterey security patches end

**Rationale:**

- Zero cost now; maintains cash flow
- Wolf-air works adequately for current workload
- Defers $500-$700 machine purchase to later

**Trade-off:**

- Security risk increases after June 2026 if still on Monterey
- Hardware aging (11-year-old battery will degrade further)

---

### Option 2: Upgrade Now to M3 Air (Recommended)

**Path:** Hunt and purchase used M3 Air 16GB this month; upgrade before Monterey EOL pressure.

1. **Search eBay, Facebook Marketplace, Swappa**
   - Timeline: 3-7 days to find + purchase
   - Cost: $500-$700
   - Viability: Primary through 2027+
   - Specs: M3 16GB RAM, 256GB+ SSD

2. **Restore from NAS Time Machine backup (2026-06-27)**
   - Timeline: 1-2 days
   - Recovers: .bashrc, .zshrc, .ssh/, git config, shell scripts, dotfiles
   - GitHub data: All code is remote; no loss
   - Data loss: None

**Timeline:**

- **Week of 2026-08-05:** Begin machine hunt
- **Week of 2026-08-12:** Purchase machine
- **2026-08-13 to 2026-08-15:** Time Machine restore
- **2026-08-16 onwards:** Operational

**Rationale:**

- Proactive; removes OS EOL pressure
- Longer machine lifespan (viable through 2027+)
- Fresh hardware + modern thermals

---

### Option 3: Upgrade to M2 Air (Budget Alternative)

**Path:** Hunt used M2 Air if M3 unavailable or cost is priority.

- Timeline: 3-7 days to find
- Cost: $400-$600
- Viability: Through 2027; older but functional
- Trade-off: Older chip than M3; less comfortable

---

## Recommendation

**Option 1 (defer)** if Michael is content with wolf-air and budget is tight. Safe through mid-2026.

**Option 2 (upgrade now)** if Michael prefers eliminating Monterey EOL pressure and wants modern hardware. Best long-term value.

---

## Summary: What Michael Actually Needs

- **macOS:** Monterey 12 works (Claude Code 2.1.221 confirmed running); Tahoe+ preferred for longevity
- **Monterey EOL:** Mid-2026 (~6 months); plan upgrade before or accept security gap after
- **RAM:** 16GB recommended (multi-file Claude Code sessions; 8GB OK for git-only)
- **CPU:** M3+ sufficient; M4/M5 overkill for light development
- **Storage:** 256GB minimum (code repos + Claude Code cache)
- **Cost ceiling:** $700 for used M3 Air (or $0 to defer and continue on wolf-air)
- **Backup freshness:** 2026-06-27 (5+ weeks old); acceptable for code/config restore

**Verdict:**

- **Short-term (through mid-2026):** wolf-air is functional and free. Acceptable interim.
- **Long-term (2026+):** M3 MacBook Air 16GB recommended ($500-$700). Eliminates Monterey EOL pressure.

---

## Backup Information

**NAS Time Machine backup date:** 2026-06-27 (38 days ago; ~5.5 weeks old)

**Data loss assessment:**

- GitHub repos: All code is remote; no loss
- Dotfiles (.bashrc, .ssh/, git config): Recovered from backup
- Shell scripts: Recovered from backup
- No critical data loss from 5+ week gap

---

## Sources

- [Claude Code System Requirements](https://houtini.com/articles/claude-code-system-requirements/)
- [Claude Code Installation macOS](https://skilzy.io/en/blog/install-claude-code-macos-guide)
- [macOS Monterey EOL](https://support.apple.com/en-us/HT211238)
- [M-series Performance Specs](https://www.anandtech.com/show/21486/the-apple-macbook-pro-m4-pro-review)
