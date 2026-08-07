# M-18 · Multi-count undo halts with guidance

| | |
|---|---|
| **LLM** | yes |
| **Ollama** | on |
| **Result** | ✅ PASS |
| **Run** | v0.3.0 · 2026-08-07 13:30 |

## Notes
'undo the last 3 commits' → no gate, no action; guidance offers squash-3 / revert / undo-most-recent; HEAD == PRE unchanged. Recognize-but-don't-act boundary holds.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
