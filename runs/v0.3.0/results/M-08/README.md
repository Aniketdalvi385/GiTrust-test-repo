# M-08 · Conflicting rebase -> calm pause -> continue (flagship)

| | |
|---|---|
| **LLM** | partial |
| **Ollama** | on |
| **Result** | ✅ PASS |
| **Run** | v0.3.0 · 2026-08-07 13:30 |

## Notes
Rebase hit the same-line conflict and paused CALMLY: names 1 file (correct count — v0.2 said '0 file(s)'), 'nothing is lost', offers continue/abort verbs, EXIT=1 (v0.2 was exit 0). Both P1 exit-code and P5 conflict-count fixes confirmed live.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
