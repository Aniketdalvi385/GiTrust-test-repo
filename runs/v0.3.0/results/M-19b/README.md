# M-19b · Squash last 3 — word "last three commits"

| | |
|---|---|
| **LLM** | yes |
| **Ollama** | on |
| **Result** | ✅ PASS |
| **Run** | v0.3.0 · 2026-08-10 16:22 (router re-run) |

## Notes
FIXED. ⚡ instant (was ◉ LLM → wrong undo-one). Spelled-out "three" now parses: squash 3, count 4→2, tree oid IDENTICAL. The M-19b v0.3.0 FAIL is resolved by the word-number capture. PASS.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
