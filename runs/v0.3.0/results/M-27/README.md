# M-27 · Fail-closed trash-net

| | |
|---|---|
| **LLM** | no |
| **Ollama** | on |
| **Result** | ✅ PASS |
| **Run** | v0.3.0 · 2026-08-07 13:31 |

## Notes
Fail-closed: with ~/.gitrust/trash chmod 000, clean REFUSED — 'Failed to create trash dir … Permission denied', EXIT=1, and keepme.txt STILL PRESENT (nothing deleted without a backup). Runner auto-restored chmod 755 after. Fail-closed invariant holds, and exits nonzero correctly.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
