# M-16 · Undo -> discard: TypeToConfirm + trash-net

| | |
|---|---|
| **LLM** | no |
| **Ollama** | on |
| **Result** | ✅ PASS |
| **Run** | v0.3.0 · 2026-08-07 13:30 |

## Notes
Discard path: 4-option gate → TypeToConfirm (typed the oid) → reset. HEAD is now 'base' — the commit was ACTUALLY DROPPED (v0.2 was a phantom no-op). Safety copy reads 'type the highlighted value' (token-neutral, M-16 copy fix). No new trash dir written because the discarded commit had no uncommitted tracked changes to back up (correct — the '20260805' dir is a stale pre-existing one). P0 reset fix + M-16 copy fix both confirmed live.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
