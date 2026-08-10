# M-04d · Scoped feature pipeline — schema scope

| | |
|---|---|
| **LLM** | yes |
| **Ollama** | on |
| **Result** | ❌ FAIL |
| **Run** | v0.3.0 · 2026-08-10 12:13 |

## Notes
MISROUTE, same as M-04b: "push all schema changes" → bare push → Stage-all→commit→push → committed ALL FOUR files (README.md, api_client.txt, migrations.sql, schema.sql). No schema scoping. Root cause: scope phrase not captured deterministically.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
