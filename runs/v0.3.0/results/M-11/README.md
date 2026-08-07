# M-11 · Mid-rebase never says checkout a branch

| | |
|---|---|
| **LLM** | yes |
| **Ollama** | on |
| **Result** | ✅ PASS |
| **Run** | v0.3.0 · 2026-08-07 13:30 |

## Notes
Mid-rebase, `commit my changes` → block names the REBASE and offers continue/abort. The words 'checkout a branch' do NOT appear — S12 regression stays dead.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
