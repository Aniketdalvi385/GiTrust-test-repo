Verdict: PASS
Summary: No panic when the pipe's reader is already gone; the run completes with exit 0 (D5).

- The runner check "no panic when the reader closes early" gives "exit=0 stderr=" (empty), and "…runs to completion: exit 0". The normal piped run shows "*  Show history", the branch line and four commits, exit 0.
- v0.4.1 notes: the FAIL is fixed. The "failed printing to stdout: Broken pipe" panic (exit 101) is gone: exit 0 with empty stderr. The "+  Show history · 2.1s" marker note no longer applies as it was, because the test now uses the exact phrase "log" (no model) and shows "*  Show history". That is the deliberate ASCII marker for piped output, not a defect.
