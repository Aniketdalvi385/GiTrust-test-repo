# M-19b · Squash last 3 — word "last three commits"

| | |
|---|---|
| **LLM** | yes |
| **Ollama** | on |
| **Result** | ❌ FAIL |
| **Run** | v0.3.0 · 2026-08-10 12:13 |

## Notes
MISROUTE, and the worst kind — WRONG OPERATION: "squash the last three commits" (count spelled as a word) fell to the LLM (◉), which routed to UNDO ONE commit (soft reset of c3). count 4→3 (expected 4→2), tree CHANGED (2d2e01a…, expected identical). The word "three" is not parsed as a count; only the digit "3" is. Contrast M-19a/c (digit) which squashed correctly.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
