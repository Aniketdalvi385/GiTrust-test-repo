# M-19 · Squash last 3: tree-identical

| | |
|---|---|
| **LLM** | yes |
| **Ollama** | on |
| **Result** | ✅ PASS |
| **Run** | v0.3.0 · 2026-08-07 13:30 |

## Notes
'squash the last 3' fast-path (*) → squash gate with combined message → count 4→2 (dropped by 2), tree oid IDENTICAL (bf23f09…). A real squash into one commit. v0.2 was a phantom single-reset no-op; P0 + P2 squash-routing fixes confirmed.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
