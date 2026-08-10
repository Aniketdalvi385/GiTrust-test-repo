# M-20b · Amend-on-pushed — "reword the last commit to …"

| | |
|---|---|
| **LLM** | llm |
| **Ollama** | on |
| **Result** | ❌ FAIL |
| **Run** | v0.3.0 · 2026-08-10 16:22 (router re-run) |

## Notes
MISROUTE (unchanged): "reword the last commit to '…'" (◉ LLM) read as a new commit → drafted "update files" → "Nothing staged" → BLOCKED. No amend, no force-push; remote subject unchanged ("typo mesage"). capture_amend_message requires "commit message" in the phrase; "reword the last commit to X" (no literal "message") is not matched, and amend is router-excluded. Known gap; candidate for capture_amend_message widening ("reword … to X").

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
