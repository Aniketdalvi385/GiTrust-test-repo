# M-13 · Detached write -> rescue

| | |
|---|---|
| **LLM** | yes |
| **Ollama** | on |
| **Result** | ⚠️ PASS (with defects) |
| **Run** | v0.3.0 · 2026-08-07 13:30 |

## Notes
Branch-here rescue works (created + switched to rescue-work, no data loss). BUT the original 'commit this' did NOT complete: pre-check blocked with 'Nothing staged to commit' — the resume reached the commit step but the change wasn't auto-staged, so the commit-continuation still doesn't land the user's edit. The M-13 resume fix wires the redirect through, but the commit needs staging. Change is safe (M app.txt on rescue-work), so PASS-with-defect, not FAIL.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
