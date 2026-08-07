# M-21 · Failing pre-commit blocks (via system git)

| | |
|---|---|
| **LLM** | yes |
| **Ollama** | on |
| **Result** | ⚠️ PASS (with defects) |
| **Run** | v0.3.0 · 2026-08-07 13:31 |

## Notes
Hook enforcement works: 'Hook(s) present (pre-commit) — using system git', commit BLOCKED, 'LINT FAILED' surfaced, count 1→1 unchanged. DEFECT: final EXIT=0 — the interactive recovery picker (Show/Cancel) was entered and 'Show' exits 0, so the blocked-commit's nonzero status is lost to a caller. The block itself is correct and no bad commit was made; the exit code after the picker is the defect (same exit-honesty family as the P1 cluster, but on the hook-block→picker path).

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
