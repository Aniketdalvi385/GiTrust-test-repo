# M-04 · Scoped feature pipeline (flagship)

| | |
|---|---|
| **LLM** | yes |
| **Ollama** | on |
| **Result** | ✅ PASS |
| **Run** | v0.3.0 · 2026-08-07 13:30 |

## Notes
Scoped routing worked (fast-path *): resolver classified login.txt=Related (pre-checked), readme.txt=Unrelated (hidden), auth.txt=Uncertain (offered, not pre-checked). Pushed commit contains only login.txt — readme correctly excluded. Note: auth.txt was left out because it was Uncertain and not toggled on; scoping itself is correct.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
