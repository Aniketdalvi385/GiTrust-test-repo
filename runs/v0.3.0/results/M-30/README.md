# M-30 · Not a repo

| | |
|---|---|
| **LLM** | no |
| **Ollama** | on |
| **Result** | ✅ PASS |
| **Run** | v0.3.0 · 2026-08-07 13:31 |

## Notes
Outside a git repo: '✗ Not inside a git repository…' friendly message, no stack trace, EXIT=1. v0.2 was exit 0 (and the earlier harness bug made the dir look like a repo). Both the P1 exit-code correctness and the harness sandbox-location fix confirmed.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
