# PATH Verification Strategy: Testing Commands, Not Just Files

## Problem

Current `.profile` logic only tests **existence** of directories/files:
```bash
if [ -x "/opt/local/bin/port" ]; then
    PATH="/opt/local/bin:${PATH}"
fi
```

**Risk:** Apple migrations can leave executable files that can't actually run (Intel binary on ARM). Files may exist and be executable, but fail when invoked.

**Example (what we hit):**
- `/opt/local/bin/port` exists ✓
- `/opt/local/bin/port` is executable ✓
- `/opt/local/bin/port --version` fails ✗ (Intel binary on ARM)

**Result:** Cruft gets added to PATH, polluting the environment

---

## Proposed Solutions

### Option A: Test Command Execution (Recommended)

```bash
# Instead of just checking existence, verify the command works
if /opt/local/bin/port --version >/dev/null 2>&1; then
    PATH="/opt/local/bin:${PATH}"
fi
```

**Pros:**
- Catches broken/incompatible binaries at startup
- Simple, direct test of actual functionality
- No false positives from migration garbage

**Cons:**
- Slightly slower (actually runs the command once at shell startup)
- Requires knowing a "safe" flag for each tool (--version, --help, etc.)

### Option B: Use `command -v` (Middle Ground)

```bash
# Test if the binary can be resolved and executed
if command -v /opt/local/bin/port >/dev/null 2>&1; then
    PATH="/opt/local/bin:${PATH}"
fi
```

**Pros:**
- Shell's built-in `command` does a smarter check than `[ -x ]`
- Works across shells (bash, zsh, sh)
- Still validates executability

**Cons:**
- Less rigorous than actually running the command
- May pass for broken binaries (depends on shell implementation)

### Option C: Architecture Check (Surgical)

```bash
# Check if binary is native architecture
# (only works on macOS with lipo; checks for arm64 or x86_64)
if [ -x "/opt/local/bin/port" ] && \
   (file /opt/local/bin/port | grep -q "arm64" || \
    file /opt/local/bin/port | grep -q "x86_64"); then
    PATH="/opt/local/bin:${PATH}"
fi
```

**Pros:**
- Catches architecture mismatches specifically
- Doesn't require running the command
- Fast (just calls `file`)

**Cons:**
- macOS-specific (uses `file` command output)
- Doesn't catch other failure modes (missing libraries, etc.)
- More complex logic

---

## Recommendation

**Option A (Test Execution)** is best because:

1. **Catches all failure modes**, not just architecture
2. **Simple logic**, easy to understand
3. **One-time cost** at shell startup (negligible)
4. **Self-documenting:** anyone reading `.profile` sees the command actually needs to work

### Implementation for wolf-air

```bash
# MacPorts: only add to PATH if port command actually works
_port_prefix="/opt/local"
if [ -x "${_port_prefix}/bin/port" ] && \
   "${_port_prefix}/bin/port" --version >/dev/null 2>&1; then
    [ -d "${_port_prefix}/bin" ]  && PATH="${_port_prefix}/bin:${PATH}"
    [ -d "${_port_prefix}/sbin" ] && PATH="${_port_prefix}/sbin:${PATH}"
fi
unset _port_prefix
```

---

## Testing This Strategy

### Before (Current: Existence Only)

```bash
# This would pass, adding x86_64 MacPorts to PATH
[ -x "/opt/local/bin/port" ] && echo "PASS: port exists"
# Output: PASS: port exists

# But running it fails
/opt/local/bin/port --version
# Output: Bad CPU type in executable
```

### After (Proposed: Execution Test)

```bash
# First check still passes
[ -x "/opt/local/bin/port" ] && echo "PASS: port exists"
# Output: PASS: port exists

# But execution test fails, so PATH not polluted
/opt/local/bin/port --version >/dev/null 2>&1 && echo "PASS" || echo "FAIL"
# Output: FAIL
```

---

## Migration & Future Machines

This strategy handles all scenarios:

| Machine                 | Scenario                        | Result                                     |
|-------------------------|---------------------------------|--------------------------------------------|
| **wolf-air** (macOS 12) | MacPorts installed, working     | `port --version` succeeds → PATH updated   |
| **michael-air** (ARM)   | /opt/local removed              | `port --version` fails → PATH skipped      |
| **Future** (any arch)   | Legacy tool broken/incompatible | Command test catches it → PATH stays clean |

---

## Decision

**Approve Option A?** Implement execution test in `.profile` to validate PATH entries actually work before using them?

This converts a "check if file exists" strategy to a "check if command works" strategy, protecting against Apple migration cruft and broken binaries.
