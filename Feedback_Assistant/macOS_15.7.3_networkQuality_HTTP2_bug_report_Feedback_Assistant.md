# networkQuality HTTP/2 Performance Bug Report

## macOS 15.7.3 (Sequoia) - Feedback Assistant Submission

**Date**: 2025-12-24  
**Tool**: networkQuality (`/usr/bin/networkQuality`)  
**macOS Version**: 15.7.3 (Build 24G419)  
**Severity**: Medium (workaround available)  
**Category**: System Tools → Networking

---

## Executive Summary

The `networkQuality` tool exhibits severe performance degradation when using HTTP/2 protocol, showing **36x worse responsiveness** compared to HTTP/1.1. The "HTTP loaded" component takes **12.2 seconds** in HTTP/2 tests, causing overall responsiveness to drop from **472 RPM (Medium)** with HTTP/1.1 to **13 RPM (Low)** with HTTP/2.

**Key Finding**: HTTP/2 "HTTP loaded" component consistently takes 4-12 seconds, while HTTP/1.1 completes without this component entirely.

**Workaround**: Use `networkQuality -f h1` flag to force HTTP/1.1 and get accurate responsiveness measurements.

---

## Problem Description

### Symptoms

When running `networkQuality` with HTTP/2 (default or forced with `-f h2`):

- **Responsiveness**: 13 RPM (Low) - **36x worse** than HTTP/1.1
- **HTTP loaded component**: 4 RPM (12.241 seconds) - **extremely slow**
- **Overall test duration**: ~48 seconds (vs ~45 seconds for HTTP/1.1)
- **Test marked as "Low accuracy"** due to poor performance

When running `networkQuality` with HTTP/1.1 (forced with `-f h1`):

- **Responsiveness**: 472 RPM (Medium) - **normal performance**
- **No "HTTP loaded" component** - test completes normally
- **Test marked as "High accuracy"** for most components

### Impact

- **Primary Impact**: `networkQuality` cannot accurately measure network responsiveness when using HTTP/2
- **Secondary Impact**: Users relying on `networkQuality` for network diagnostics may get misleading "Low" responsiveness scores
- **Workaround Available**: Yes - use `-f h1` flag

### Steps to Reproduce

1. Run: `networkQuality -f h2 -v`
2. Observe: Responsiveness shows "Low" with 13 RPM
3. Observe: "HTTP loaded" component takes 12+ seconds
4. Compare: Run `networkQuality -f h1 -v`
5. Observe: Responsiveness shows "Medium" with 472 RPM
6. Observe: No "HTTP loaded" component exists

**Reproducibility**: 100% - occurs consistently on every HTTP/2 test

---

## Technical Details

### Test Results Comparison

| Metric | HTTP/2 | HTTP/1.1 | Difference |
| --- | --- | --- | --- |
| **Responsiveness** | 13 RPM (Low) | 472 RPM (Medium) | **36x worse** |
| **HTTP loaded** | 4 RPM (12.241s) | N/A (doesn't exist) | **N/A** |
| **Transport** | 1068 RPM (56ms) | 85 RPM (700ms) | HTTP/1.1 slower here |
| **Security (TLS)** | 149 RPM (402ms) | 106 RPM (565ms) | HTTP/1.1 slower here |
| **HTTP** | 710 RPM (84ms) | 335 RPM (179ms) | HTTP/1.1 slower here |
| **Idle Latency** | 1319 RPM (45ms) | 1036 RPM (58ms) | HTTP/2 better |
| **Test Duration** | ~48 seconds | ~45 seconds | Similar |

**Key Observation**: The "HTTP loaded" component (12.2 seconds) is the primary bottleneck in HTTP/2 tests. This component does not exist in HTTP/1.1 tests.

### System Configuration

- **macOS**: 15.7.3 (Build 24G419)
- **Hardware**: MacBook Pro 16,2 (Intel Core i5-1038NG7)
- **Network Interface**: en0 (WiFi)
- **Firewall**: LuLu firewall active (but issue persists with firewall disabled)
- **Test Endpoint**: usmia1-edge-fx-032.aaplimg.com (HTTP/2), usmia1-edge-fx-002.aaplimg.com (HTTP/1.1)

### Related Components

- **networkQuality**: Uses `NetworkQualityServices.framework` (private framework)
- **CFNetwork**: System logs show HTTP/2 tasks marked as "failure" even when `response_status=200`
- **curl HTTP/2**: Works perfectly (uses libcurl/nghttp2, not CFNetwork)

### Evidence Files

1. **[System Diagnostics](./macOS_15.7.3_networkQuality_HTTP2_system_diagnostics.md)** - Complete system information
2. **[Log Analysis](./macOS_15.7.3_networkQuality_HTTP2_log_analysis.md)** - CFNetwork logs showing HTTP/2 task failures

---

## For Bug Triage Specialists

### Classification

- **Component**: System Tools → networkQuality
- **Area**: Networking → HTTP/2 Performance
- **Severity**: Medium (workaround available, tool-specific issue)
- **Priority**: Medium (affects diagnostic tool accuracy, not core functionality)

### Key Questions Answered

1. **Is this reproducible?** Yes - 100% reproducible
2. **Is there a workaround?** Yes - use `-f h1` flag
3. **Does this affect other apps?** Unknown - only tested networkQuality tool
4. **Is this a regression?** Unknown - need comparison with macOS Monterey
5. **Is HTTP/2 broken system-wide?** No - curl HTTP/2 works fine

### Recommended Actions

1. **Verify on macOS Monterey** - Compare HTTP/2 performance to determine if this is a Sequoia regression
2. **Test other CFNetwork-based apps** - Check if Safari/Mail HTTP/2 performance is affected
3. **Review networkQuality test methodology** - The "HTTP loaded" component may be waiting for HTTP/2-specific features that aren't necessary

---

## For Developers

### Root Cause Hypothesis

The "HTTP loaded" component in networkQuality's HTTP/2 test appears to be waiting for something that:

1. Takes 4-12 seconds to complete
2. Doesn't exist in HTTP/1.1 (component doesn't appear)
3. May be HTTP/2-specific (server push, stream completion, connection multiplexing)

### System Logs Analysis

CFNetwork logs show:

- HTTP/2 tasks marked as "failure" even when `response_status=200` (successful)
- Transaction durations: 30-44 seconds for some HTTP/2 tasks
- Many tasks show `response_duration_ms=0` despite successful responses

This suggests networkQuality may be:

- Timing out HTTP/2 tasks prematurely
- Waiting for HTTP/2 features that don't arrive
- Misinterpreting HTTP/2 connection state

### Code Paths to Investigate

1. **NetworkQualityServices framework**: HTTP/2 test implementation
2. **CFNetwork HTTP/2 handling**: Connection multiplexing, stream management
3. **"HTTP loaded" component**: What is it waiting for? Why doesn't it exist in HTTP/1.1?

### Comparison Data

- **curl HTTP/2**: Works perfectly (uses libcurl/nghttp2)
- **networkQuality HTTP/1.1**: Works perfectly (472 RPM)
- **networkQuality HTTP/2**: Broken (13 RPM, 12s HTTP loaded delay)

This suggests the issue is in networkQuality's HTTP/2 test methodology, not CFNetwork itself.

---

## Step-by-Step Submission Instructions

### Step 1: Launch Feedback Assistant

```bash
open -a "Feedback Assistant"
```

Or search Spotlight for "Feedback Assistant"

### Step 2: Sign In

- Sign in with your Apple ID
- If you don't have an account, create one (free)

### Step 3: Create New Feedback

1. Click **"Create New Feedback"** or **"+"** button
2. Select **"macOS"** as the product
3. Select **"System Tools"** or **"Networking"** as the category

### Step 4: Fill Out Form

**Title**:

```text
networkQuality HTTP/2 performance severely degraded - 36x slower than HTTP/1.1
```

**Description** (copy from "Problem Description" section above):

```text
[Paste the Problem Description section]
```

**Steps to Reproduce** (copy from above):

```bash
1. Run: networkQuality -f h2 -v
2. Observe: Responsiveness shows "Low" with 13 RPM
3. Observe: "HTTP loaded" component takes 12+ seconds
4. Compare: Run networkQuality -f h1 -v
5. Observe: Responsiveness shows "Medium" with 472 RPM
6. Observe: No "HTTP loaded" component exists
```

**Expected Behavior**:

```text
HTTP/2 should perform similarly to HTTP/1.1, or at least not 36x worse. The "HTTP loaded" component should not take 12+ seconds.
```

**Actual Behavior**:

```text
HTTP/2 responsiveness is 13 RPM (Low) vs 472 RPM (Medium) with HTTP/1.1. The "HTTP loaded" component takes 12.2 seconds in HTTP/2 tests but doesn't exist in HTTP/1.1 tests.
```

**Workaround**:

```text
Use networkQuality -f h1 flag to force HTTP/1.1 and get accurate responsiveness measurements.
```

### Step 5: Attach Files

Attach the following files (if Feedback Assistant allows file attachments):

1. **System Diagnostics**: `macOS_15.7.3_networkQuality_HTTP2_system_diagnostics.md`
2. **Log Analysis**: `macOS_15.7.3_networkQuality_HTTP2_log_analysis.md`
3. **Verbose Output (HTTP/2)**: Copy from `networkQuality -f h2 -v` output
4. **Verbose Output (HTTP/1.1)**: Copy from `networkQuality -f h1 -v` output

**If file attachments aren't supported**, paste the contents of the diagnostic files into the "Additional Information" field.

### Step 6: Include System Information

Feedback Assistant should automatically include system information, but verify:

- macOS Version: 15.7.3 (Build 24G419)
- Hardware: MacBook Pro 16,2
- Network Interface: WiFi (en0)

### Step 7: Submit

1. Review all information
2. Click **"Submit"** or **"Send"**
3. Save the feedback number for future reference

---

## Additional Information

### Related Documentation

- networkQuality man page references: <https://support.apple.com/kb/HT212313>
- Apple Developer Bug Reporting: <https://developer.apple.com/bug-reporting/>

### Test Commands Reference

```bash
# Reproduce HTTP/2 issue
networkQuality -f h2 -v

# Compare with HTTP/1.1 (works correctly)
networkQuality -f h1 -v

# Collect CFNetwork logs
log show --predicate 'subsystem == "com.apple.CFNetwork" AND process == "networkQuality"' --last 2h --style compact > cfnetwork_logs.txt
```

### Contact Information

If Apple needs additional information or wants to discuss this issue:

- This bug report was prepared on 2025-12-24
- All diagnostic data is included in the referenced files
- Reproducible 100% of the time on this system

---

## Changelog

- **2025-12-24**: Initial bug report created with comprehensive diagnostics
