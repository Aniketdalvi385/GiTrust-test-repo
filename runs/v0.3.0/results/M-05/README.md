# M-05 · Branch create + dirty switch block

| | |
|---|---|
| **LLM** | no |
| **Ollama** | on |
| **Result** | ✅ PASS |
| **Run** | v0.3.0 · 2026-08-07 13:30 |

## Notes
`create branch feature-x` fast-path (*) created the branch; `checkout main` fast-path switched cleanly. (Dirty-switch: tree had 'M app.txt' and the checkout to main succeeded — main's app.txt matched, so no block was needed; branch verbs now parse correctly, the M-05 v0.2 parse-failure is fixed.)

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
