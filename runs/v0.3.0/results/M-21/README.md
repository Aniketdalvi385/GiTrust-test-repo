# M-21 · Failing pre-commit blocks (via system git)

| | |
|---|---|
| **LLM** | yes |
| **Ollama** | on |
| **Result** | ✅ PASS |
| **Run** | v0.3.0 · 2026-08-07 15:11 (re-run after fix) |

## What to look for
PASS = hooks-detected info line, commit BLOCKED, "LINT FAILED" surfaced, count unchanged, EXIT nonzero.

## Command
```bash
$GITRUST "commit this"; echo "EXIT=$?"
```

## Notes
FIXED. Hook enforcement + honest exit code both hold. Live: 'Hook(s) present (pre-commit) — using system git', commit BLOCKED, 'LINT FAILED' surfaced, count 1→1 unchanged, 'Show' picked on the recovery picker — and now **EXIT=1** (was EXIT=0 in the first v0.3.0 run). The recovery picker's informational rows (Show/Cancel) no longer swallow the failure into a success: handle_classified_recovery returns NotResolved for them, so execute_pipeline propagates last_error and exits nonzero. Regression tests: hook_rejected_commit_show_recovery_still_errors, hook_rejected_commit_cancel_recovery_reports_not_resolved. Minor: a stray "interrupted pipeline was found" banner appeared at the top from a leftover snapshot in ~/.gitrust/snapshots (unrelated to this test; honest and points at --recover). No data written; not a defect.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
