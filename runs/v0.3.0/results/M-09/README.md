# M-09 · Abort restores exactly

| | |
|---|---|
| **LLM** | no |
| **Ollama** | on |
| **Result** | ✅ PASS |
| **Run** | v0.3.0 · 2026-08-07 13:30 |

## Notes
abort rebase restored HEAD to exactly PRE (9bf9124…), tree back to [ahead 1, behind 1]. (Note: the pre-existing interrupted-pipeline snapshot warning showed — carried over from M-08's paused rebase; abort itself is clean.)

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
