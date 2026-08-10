# M-20b · Amend-on-pushed — "reword the last commit to …"

| | |
|---|---|
| **LLM** | yes |
| **Ollama** | on |
| **Result** | ❌ FAIL |
| **Run** | v0.3.0 · 2026-08-10 12:13 |

## Notes
MISROUTE: "reword the last commit to '…'" fell to the LLM (◉), which read it as a NEW commit, drafted "update files", hit "Nothing staged", and BLOCKED. No amend, no force-push; remote subject unchanged ("typo mesage"). The verb "reword" is not a recognized amend-message trigger; only "fix the last commit message to" / "change my last commit message to" fast-path. Same root cause as the other misroutes.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
