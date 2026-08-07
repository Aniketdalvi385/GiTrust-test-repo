# M-15 · Undo gate: four options, names the commit

| | |
|---|---|
| **LLM** | no |
| **Ollama** | on |
| **Result** | ✅ PASS |
| **Run** | v0.3.0 · 2026-08-07 13:30 |

## Notes
Undo gate showed exactly FOUR options, question named short oid + 'feat: the mistake'. Chose Keep-staged → commit removed, 'M  app.txt' staged (log shows only base). Correct.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
