# Log Analysis

## networkQuality HTTP/2 Performance Bug

## macOS 15.7.3 (Sequoia)

**Back to**: [Main Bug Report](./macOS_15.7.3_networkQuality_HTTP2_bug_report_Feedback_Assistant.md)

---

## Overview

This document contains analysis of CFNetwork system logs during networkQuality HTTP/2 tests. The logs reveal HTTP/2 tasks being marked as "failure" even when they complete successfully with `response_status=200`.

---

## Log Collection Method

**Command Used**:

```bash
log show --predicate 'subsystem == "com.apple.CFNetwork" AND process == "networkQuality"' --last 2h --style compact
```

**Time Range**: Last 2 hours  
**Subsystem**: com.apple.CFNetwork  
**Process**: networkQuality  
**Format**: Compact style

---

## Key Findings

### 1. HTTP/2 Tasks Marked as "Failure" Despite Success

**Pattern Observed**: CFNetwork logs show HTTP/2 tasks marked as "failure" even when:

- `response_status=200` (successful HTTP response)
- Tasks complete successfully
- Data is transferred correctly

**Example Log Entry**:

```text
[com.apple.CFNetwork:Summary] Task <...> summary for task failure {
  transaction_duration_ms=41525,
  response_status=200,
  connection=25,
  protocol="h2",
  ...
}
```

**Analysis**: This suggests networkQuality may be:

- Timing out HTTP/2 tasks prematurely
- Misinterpreting HTTP/2 connection state
- Waiting for HTTP/2 features that don't arrive

### 2. Long Transaction Durations

**Observed Durations**: 30-44 seconds for HTTP/2 tasks

**Comparison**: HTTP/1.1 tasks typically complete in <1 second

**Impact**: These long durations contribute to the "HTTP loaded" component taking 12+ seconds

### 3. Zero Response Duration Despite Success

**Pattern**: Many HTTP/2 tasks show:

- `response_status=200` (successful)
- `response_duration_ms=0` (zero duration)
- Task marked as "failure"

**Analysis**: This suggests the response is received but networkQuality doesn't recognize it as complete, causing it to wait for additional data or signals.

---

## Sample Log Entries

### Successful HTTP/2 Task (Marked as Failure)

```text
2025-12-24 14:52:31.810 Df networkQuality[93962:38d112] 
[com.apple.CFNetwork:Summary] Task <B7C2DC2C-4ECA-4181-8F37-C2A04F0E0A04>.<1> 
summary for task success {
  transaction_duration_ms=120,
  response_status=200,
  connection=41,
  protocol="h2",
  domain_lookup_duration_ms=1,
  connect_duration_ms=89,
  secure_connection_duration_ms=70,
  private_relay=false,
  request_start_ms=94,
  request_duration_ms=0,
  response_start_ms=119,
  response_duration_ms=0,
  request_bytes=114,
  request_throughput_kbps=1002,
  response_bytes=193,
  response_throughput_kbps=763,
  cache_hit=false
}
```

**Note**: This task shows "success" but many others show "failure" with similar characteristics.

### HTTP/2 Connection Lifecycle

```text
2025-12-24 14:52:31.806 Df networkQuality[93962:38d113] 
[com.apple.CFNetwork:Default] Connection 42: enabling TLS

2025-12-24 14:52:31.807 Df networkQuality[93962:38d113] 
[com.apple.CFNetwork:Default] Connection 42: starting, TC(0x0)

2025-12-24 14:52:31.901 Df networkQuality[93962:38d112] 
[com.apple.CFNetwork:Default] Connection 42: asked to evaluate TLS Trust

2025-12-24 14:52:31.911 Df networkQuality[93962:38d113] 
[com.apple.CFNetwork:Default] Connection 42: TLS Trust result 0

2025-12-24 14:52:31.912 Df networkQuality[93962:38d113] 
[com.apple.CFNetwork:Default] Connection 42: connected successfully

2025-12-24 14:52:31.912 Df networkQuality[93962:38d113] 
[com.apple.CFNetwork:Default] Connection 42: TLS handshake complete

2025-12-24 14:52:31.912 Df networkQuality[93962:38d113] 
[com.apple.CFNetwork:Default] Connection 42: ready C(N) E(N)

2025-12-24 14:52:31.912 Df networkQuality[93962:38d113] 
[com.apple.CFNetwork:Default] Task <03D26E16-3499-4E32-A5D5-C9E30DD7989E>.<1> sent request, body N 0

2025-12-24 14:52:31.943 Df networkQuality[93962:38d118] 
[com.apple.CFNetwork:Default] Task <03D26E16-3499-4E32-A5D5-C9E30DD7989E>.<1> received response, status 200 content K

2025-12-24 14:52:31.943 Df networkQuality[93962:38d113] 
[com.apple.CFNetwork:Summary] Task <03D26E16-3499-4E32-A5D5-C9E30DD7989E>.<1> 
summary for task success {
  transaction_duration_ms=137,
  response_status=200,
  connection=42,
  protocol="h2",
  ...
}
```

**Analysis**: Individual HTTP/2 connections establish and complete successfully. The issue appears to be in networkQuality's aggregation or interpretation of these connections.

---

## Full Log Sample (Last 100 Lines)

```text
2025-12-24 14:52:31.719 Df networkQuality[93962:38d116] [com.apple.CFNetwork:Default] Connection 40: cleaning up
2025-12-24 14:52:31.719 Df networkQuality[93962:38d116] [com.apple.CFNetwork:Default] Connection 40: done
2025-12-24 14:52:31.719 Df networkQuality[93977:38d159] [com.apple.CFNetwork:Default] Connection 14: done
2025-12-24 14:52:31.719 Df networkQuality[93977:38d159] [com.apple.CFNetwork:Default] Connection 14: done
2025-12-24 14:52:31.773 Df networkQuality[93962:38d116] [com.apple.CFNetwork:Default] Connection 41: asked to evaluate TLS Trust
2025-12-24 14:52:31.773 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Task <B7C2DC2C-4ECA-4181-8F37-C2A04F0E0A04>.<1> auth completion disp=1 cred=0x0
2025-12-24 14:52:31.782 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Connection 41: TLS Trust result 0
2025-12-24 14:52:31.783 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Connection 41: connected successfully
2025-12-24 14:52:31.783 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Connection 41: TLS handshake complete
2025-12-24 14:52:31.783 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Connection 41: ready C(N) E(N)
2025-12-24 14:52:31.783 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Task <B7C2DC2C-4ECA-4181-8F37-C2A04F0E0A04>.<1> now using Connection 41
2025-12-24 14:52:31.783 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Connection 41: received viability advisory(Y)
2025-12-24 14:52:31.783 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Task <B7C2DC2C-4ECA-4181-8F37-C2A04F0E0A04>.<1> sent request, body N 0
2025-12-24 14:52:31.805 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Task <03D26E16-3499-4E32-A5D5-C9E30DD7989E>.<1> resuming, timeouts(60.0, 604800.0) qos(0x11) voucher((null)) activity(00000000-0000-0000-0000-000000000000)
2025-12-24 14:52:31.805 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Task <A0F669C3-EB84-402B-BDB2-320F5ACFB6A6>.<7> resuming, timeouts(60.0, 604800.0) qos(0x11) voucher((null)) activity(00000000-0000-0000-0000-000000000000)
2025-12-24 14:52:31.806 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Connection 42: enabling TLS
2025-12-24 14:52:31.806 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Connection 42: starting, TC(0x0)
2025-12-24 14:52:31.807 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Task <03D26E16-3499-4E32-A5D5-C9E30DD7989E>.<1> setting up Connection 42
2025-12-24 14:52:31.808 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Task <A0F669C3-EB84-402B-BDB2-320F5ACFB6A6>.<7> now using Connection 24
2025-12-24 14:52:31.808 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Task <A0F669C3-EB84-402B-BDB2-320F5ACFB6A6>.<7> sent request, body N 0
2025-12-24 14:52:31.809 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Task <B7C2DC2C-4ECA-4181-8F37-C2A04F0E0A04>.<1> received response, status 200 content K
2025-12-24 14:52:31.809 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Task <B7C2DC2C-4ECA-4181-8F37-C2A04F0E0A04>.<1> done using Connection 41
2025-12-24 14:52:31.810 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Task <B7C2DC2C-4ECA-4181-8F37-C2A04F0E0A04>.<1> response ended
2025-12-24 14:52:31.810 Df networkQuality[93962:38d112] [com.apple.CFNetwork:Summary] Task <B7C2DC2C-4ECA-4181-8F37-C2A04F0E0A04>.<1> summary for task success {transaction_duration_ms=120, response_status=200, connection=41, protocol="h2", domain_lookup_duration_ms=1, connect_duration_ms=89, secure_connection_duration_ms=70, private_relay=false, request_start_ms=94, request_duration_ms=0, response_start_ms=119, response_duration_ms=0, request_bytes=114, request_throughput_kbps=1002, response_bytes=193, response_throughput_kbps=763, cache_hit=false}
2025-12-24 14:52:31.810 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Task <B7C2DC2C-4ECA-4181-8F37-C2A04F0E0A04>.<1> finished successfully
2025-12-24 14:52:31.811 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Connection 41: cleaning up
2025-12-24 14:52:31.811 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Connection 41: done
2025-12-24 14:52:31.901 Df networkQuality[93962:38d112] [com.apple.CFNetwork:Default] Connection 42: asked to evaluate TLS Trust
2025-12-24 14:52:31.901 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Task <03D26E16-3499-4E32-A5D5-C9E30DD7989E>.<1> auth completion disp=1 cred=0x0
2025-12-24 14:52:31.911 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Connection 42: TLS Trust result 0
2025-12-24 14:52:31.912 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Connection 42: connected successfully
2025-12-24 14:52:31.912 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Connection 42: TLS handshake complete
2025-12-24 14:52:31.912 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Connection 42: ready C(N) E(N)
2025-12-24 14:52:31.912 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Task <03D26E16-3499-4E32-A5D5-C9E30DD7989E>.<1> now using Connection 42
2025-12-24 14:52:31.912 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Connection 42: received viability advisory(Y)
2025-12-24 14:52:31.912 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Task <03D26E16-3499-4E32-A5D5-C9E30DD7989E>.<1> sent request, body N 0
2025-12-24 14:52:31.923 Df networkQuality[93962:38d116] [com.apple.CFNetwork:Default] Task <C6250B74-721C-4747-9794-EBA124E7F825>.<1> resuming, timeouts(60.0, 604800.0) qos(0x11) voucher((null)) activity(00000000-0000-0000-0000-000000000000)
2025-12-24 14:52:31.923 Df networkQuality[93962:38d116] [com.apple.CFNetwork:Default] Task <2EFF6748-41FB-46C7-9E02-E5E5900B05BD>.<12> resuming, timeouts(60.0, 604800.0) qos(0x11) voucher((null)) activity(00000000-0000-0000-0000-000000000000)
2025-12-24 14:52:31.924 Df networkQuality[93962:38d118] [com.apple.CFNetwork:Default] Task <2EFF6748-41FB-46C7-9E02-E5E5900B05BD>.<12> now using Connection 12
2025-12-24 14:52:31.924 Df networkQuality[93962:38d118] [com.apple.CFNetwork:Default] Task <2EFF6748-41FB-46C7-9E02-E5E5900B05BD>.<12> sent request, body N 0
2025-12-24 14:52:31.924 Df networkQuality[93962:38d118] [com.apple.CFNetwork:Default] Connection 43: enabling TLS
2025-12-24 14:52:31.924 Df networkQuality[93962:38d118] [com.apple.CFNetwork:Default] Connection 43: starting, TC(0x0)
2025-12-24 14:52:31.925 Df networkQuality[93962:38d118] [com.apple.CFNetwork:Default] Task <C6250B74-721C-4747-9794-EBA124E7F825>.<1> setting up Connection 43
2025-12-24 14:52:31.943 Df networkQuality[93962:38d118] [com.apple.CFNetwork:Default] Task <03D26E16-3499-4E32-A5D5-C9E30DD7989E>.<1> received response, status 200 content K
2025-12-24 14:52:31.943 Df networkQuality[93962:38d118] [com.apple.CFNetwork:Default] Task <03D26E16-3499-4E32-A5D5-C9E30DD7989E>.<1> done using Connection 42
2025-12-24 14:52:31.943 Df networkQuality[93962:38d118] [com.apple.CFNetwork:Default] Task <03D26E16-3499-4E32-A5D5-C9E30DD7989E>.<1> response ended
2025-12-24 14:52:31.943 Df networkQuality[93962:38d112] [com.apple.CFNetwork:Summary] Task <03D26E16-3499-4E32-A5D5-C9E30DD7989E>.<1> summary for task success {transaction_duration_ms=137, response_status=200, connection=42, protocol="h2", domain_lookup_duration_ms=1, connect_duration_ms=103, secure_connection_duration_ms=73, private_relay=false, request_start_ms=106, request_duration_ms=0, response_start_ms=137, response_duration_ms=0, request_bytes=114, request_throughput_kbps=1185, response_bytes=193, response_throughput_kbps=889, cache_hit=false}
2025-12-24 14:52:31.943 Df networkQuality[93962:38d112] [com.apple.CFNetwork:Default] Task <03D26E16-3499-4E32-A5D5-C9E30DD7989E>.<1> finished successfully
2025-12-24 14:52:31.944 Df networkQuality[93962:38d116] [com.apple.CFNetwork:Default] Connection 42: cleaning up
2025-12-24 14:52:31.944 Df networkQuality[93962:38d116] [com.apple.CFNetwork:Default] Connection 42: done
2025-12-24 14:52:32.007 Df networkQuality[93962:38d112] [com.apple.CFNetwork:Default] Connection 43: asked to evaluate TLS Trust
2025-12-24 14:52:32.007 Df networkQuality[93962:38d112] [com.apple.CFNetwork:Default] Connection 43: asked to evaluate TLS Trust
2025-12-24 14:52:32.007 Df networkQuality[93962:38d116] [com.apple.CFNetwork:Default] Task <C6250B74-721C-4747-9794-EBA124E7F825>.<1> auth completion disp=1 cred=0x0
2025-12-24 14:52:32.007 Df networkQuality[93962:38d116] [com.apple.CFNetwork:Default] Task <C6250B74-721C-4747-9794-EBA124E7F825>.<1> auth completion disp=1 cred=0x0
2025-12-24 14:52:32.019 Df networkQuality[93962:38d112] [com.apple.CFNetwork:Default] Connection 43: TLS Trust result 0
2025-12-24 14:52:32.019 Df networkQuality[93962:38d112] [com.apple.CFNetwork:Default] Connection 43: TLS Trust result 0
2025-12-24 14:52:32.021 Df networkQuality[93962:38d112] [com.apple.CFNetwork:Default] Connection 43: connected successfully
2025-12-24 14:52:32.021 Df networkQuality[93962:38d112] [com.apple.CFNetwork:Default] Connection 43: connected successfully
2025-12-24 14:52:32.021 Df networkQuality[93962:38d112] [com.apple.CFNetwork:Default] Connection 43: TLS handshake complete
2025-12-24 14:52:32.021 Df networkQuality[93962:38d112] [com.apple.CFNetwork:Default] Connection 43: TLS handshake complete
2025-12-24 14:52:32.021 Df networkQuality[93962:38d112] [com.apple.CFNetwork:Default] Connection 43: ready C(N) E(N)
2025-12-24 14:52:32.021 Df networkQuality[93962:38d112] [com.apple.CFNetwork:Default] Connection 43: ready C(N) E(N)
2025-12-24 14:52:32.021 Df networkQuality[93962:38d112] [com.apple.CFNetwork:Default] Task <C6250B74-721C-4747-9794-EBA124E7F825>.<1> now using Connection 43
2025-12-24 14:52:32.021 Df networkQuality[93962:38d112] [com.apple.CFNetwork:Default] Task <C6250B74-721C-4747-9794-EBA124E7F825>.<1> now using Connection 43
2025-12-24 14:52:32.021 Df networkQuality[93962:38d112] [com.apple.CFNetwork:Default] Connection 43: received viability advisory(Y)
2025-12-24 14:52:32.021 Df networkQuality[93962:38d112] [com.apple.CFNetwork:Default] Connection 43: received viability advisory(Y)
2025-12-24 14:52:32.022 Df networkQuality[93962:38d112] [com.apple.CFNetwork:Default] Task <C6250B74-721C-4747-9794-EBA124E7F825>.<1> sent request, body N 0
2025-12-24 14:52:32.022 Df networkQuality[93962:38d112] [com.apple.CFNetwork:Default] Task <C6250B74-721C-4747-9794-EBA124E7F825>.<1> sent request, body N 0
2025-12-24 14:52:32.038 Df networkQuality[93962:38d116] [com.apple.CFNetwork:Default] Task <5848F934-85B6-4F48-BED4-2A1D464ADAD2>.<8> received response, status 200 content K
2025-12-24 14:52:32.038 Df networkQuality[93962:38d116] [com.apple.CFNetwork:Default] Task <5848F934-85B6-4F48-BED4-2A1D464ADAD2>.<8> received response, status 200 content K
2025-12-24 14:52:32.038 Df networkQuality[93962:38d116] [com.apple.CFNetwork:Default] Task <9A61F50B-F449-458F-B236-203456F80430>.<9> received response, status 200 content K
2025-12-24 14:52:32.038 Df networkQuality[93962:38d116] [com.apple.CFNetwork:Default] Task <9A61F50B-F449-458F-B236-203456F80430>.<9> received response, status 200 content K
2025-12-24 14:52:32.038 Df networkQuality[93962:38d118] [com.apple.CFNetwork:Default] Task <06EDD9B9-5FC3-4A49-B336-D2FA6F64F137>.<1> resuming, timeouts(60.0, 604800.0) qos(0x11) voucher((null)) activity(00000000-0000-0000-0000-000000000000)
2025-12-24 14:52:32.038 Df networkQuality[93962:38d118] [com.apple.CFNetwork:Default] Task <06EDD9B9-5FC3-4A49-B336-D2FA6F64F137>.<1> resuming, timeouts(60.0, 604800.0) qos(0x11) voucher((null)) activity(00000000-0000-0000-0000-000000000000)
2025-12-24 14:52:32.038 Df networkQuality[93962:38d118] [com.apple.CFNetwork:Default] Task <CA0ED410-97E7-4E5D-ABD5-EBFC26ED4094>.<2> resuming, timeouts(60.0, 604800.0) qos(0x11) voucher((null)) activity(00000000-0000-0000-0000-000000000000)
2025-12-24 14:52:32.038 Df networkQuality[93962:38d118] [com.apple.CFNetwork:Default] Task <CA0ED410-97E7-4E5D-ABD5-EBFC26ED4094>.<2> resuming, timeouts(60.0, 604800.0) qos(0x11) voucher((null)) activity(00000000-0000-0000-0000-000000000000)
2025-12-24 14:52:32.039 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Task <CA0ED410-97E7-4E5D-ABD5-EBFC26ED4094>.<2> now using Connection 35
2025-12-24 14:52:32.039 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Task <CA0ED410-97E7-4E5D-ABD5-EBFC26ED4094>.<2> now using Connection 35
2025-12-24 14:52:32.039 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Connection 44: enabling TLS
2025-12-24 14:52:32.039 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Connection 44: enabling TLS
2025-12-24 14:52:32.039 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Connection 44: starting, TC(0x0)
2025-12-24 14:52:32.039 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Connection 44: starting, TC(0x0)
2025-12-24 14:52:32.040 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Task <06EDD9B9-5FC3-4A49-B336-D2FA6F64F137>.<1> setting up Connection 44
2025-12-24 14:52:32.040 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Task <06EDD9B9-5FC3-4A49-B336-D2FA6F64F7F64F137>.<1> setting up Connection 44
2025-12-24 14:52:32.040 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Task <CA0ED410-97E7-4E5D-ABD5-EBFC26ED4094>.<2> sent request, body N 0
2025-12-24 14:52:32.040 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Task <CA0ED410-97E7-4E5D-ABD5-EBFC26ED4094>.<2> sent request, body N 0
2025-12-24 14:52:32.053 Df networkQuality[93962:38d119] [com.apple.CFNetwork:Default] Task <C6250B74-721C-4747-9794-EBA124E7F825>.<1> received response, status 200 content K
2025-12-24 14:52:32.053 Df networkQuality[93962:38d119] [com.apple.CFNetwork:Default] Task <C6250B74-721C-4747-9794-EBA124E7F825>.<1> received response, status 200 content K
2025-12-24 14:52:32.053 Df networkQuality[93962:38d119] [com.apple.CFNetwork:Default] Task <C6250B74-721C-4747-9794-EBA124E7F825>.<1> done using Connection 43
2025-12-24 14:52:32.053 Df networkQuality[93962:38d119] [com.apple.CFNetwork:Default] Task <C6250B74-721C-4747-9794-EBA124E7F825>.<1> done using Connection 43
2025-12-24 14:52:32.053 Df networkQuality[93962:38d119] [com.apple.CFNetwork:Default] Task <C6250B74-721C-4747-9794-EBA124E7F825>.<1> response ended
2025-12-24 14:52:32.053 Df networkQuality[93962:38d119] [com.apple.CFNetwork:Default] Task <C6250B74-721C-4747-9794-EBA124E7F825>.<1> response ended
2025-12-24 14:52:32.053 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Summary] Task <C6250B74-721C-4747-9794-EBA124E7F825>.<1> summary for task success {transaction_duration_ms=130, response_status=200, connection=43, protocol="h2", domain_lookup_duration_ms=1, connect_duration_ms=94, secure_connection_duration_ms=75, private_relay=false, request_start_ms=98, request_duration_ms=0, response_start_ms=129, response_duration_ms=0, request_bytes=114, request_throughput_kbps=416, response_bytes=193, response_throughput_kbps=394, cache_hit=false}
2025-12-24 14:52:32.053 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Task <C6250B74-721C-4747-9794-EBA124E7F825>.<1> finished successfully
2025-12-24 14:52:32.053 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Task <C6250B74-721C-4747-9794-EBA124E7F825>.<1> finished successfully
2025-12-24 14:52:32.054 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Connection 43: cleaning up
2025-12-24 14:52:32.054 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Connection 43: cleaning up
2025-12-24 14:52:32.055 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Connection 43: done
2025-12-24 14:52:32.055 Df networkQuality[93962:38d113] [com.apple.CFNetwork:Default] Connection 43: done
```

---

## Analysis Summary

### Patterns Identified

1. **Individual HTTP/2 connections work correctly**: TLS handshakes complete, requests are sent, responses (status 200) are received
2. **Tasks marked as "success"**: Many individual tasks complete successfully
3. **Long transaction durations**: Some tasks take 30-44 seconds (observed in earlier logs)
4. **Zero response duration**: Many tasks show `response_duration_ms=0` despite successful responses

### Hypothesis

The issue appears to be in networkQuality's **aggregation or interpretation** of HTTP/2 connections, not in CFNetwork's HTTP/2 implementation itself. The "HTTP loaded" component may be:

1. Waiting for HTTP/2-specific features (server push, stream completion signals)
2. Timing out while waiting for additional data
3. Misinterpreting HTTP/2 connection multiplexing state
4. Incorrectly calculating completion time for HTTP/2 streams

### Recommendations for Developers

1. **Review networkQuality's HTTP/2 test implementation** in NetworkQualityServices framework
2. **Compare HTTP/1.1 vs HTTP/2 test completion logic** - why doesn't "HTTP loaded" exist in HTTP/1.1?
3. **Investigate what "HTTP loaded" is waiting for** - is it necessary for accurate responsiveness measurement?
4. **Check timeout values** - are HTTP/2 tasks timing out prematurely?

---

## End of Log Analysis
