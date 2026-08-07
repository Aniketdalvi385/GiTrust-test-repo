# M-17 · --yes cannot undo

| | |
|---|---|
| **LLM** | no |
| **Ollama** | on |
| **Result** | ✅ PASS |
| **Run** | v0.3.0 · 2026-08-07 13:30 |

## Notes
`--yes undo` refused with EXIT=1 (v0.2 was exit 0); refusal echoes the actual gate question ('Undo ff54d5e "to undo" — what should happen…'), NOT the old wrong 'rebase vs merge' copy. HEAD == PRE (untouched). P1 exit-code + M-17 copy fix confirmed.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
