# M-20b · Amend-on-pushed — "reword the last commit to …"

| | |
|---|---|
| **LLM** | no |
| **Ollama** | on |
| **Result** | ✅ PASS |
| **Run** | v0.3.0 · 2026-08-10 16:40 (capture-fix re-run) |

## Notes
FIXED. ⚡ instant (was ◉ LLM → misread as new commit → blocked). capture_amend_message now accepts the reword/rename shape without the literal word "message". Full flagship fired: published-detection → TypeToConfirm → --force-with-lease. Remote subject = "cleaner subject line".

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
