# M-04b · Scoped feature pipeline — docs scope

| | |
|---|---|
| **LLM** | yes |
| **Ollama** | on |
| **Result** | ❌ FAIL |
| **Run** | v0.3.0 · 2026-08-10 12:13 |

## Notes
MISROUTE: "push all docs changes" was classified as a BARE push (◉ LLM), not a scoped pipeline. Hit "nothing committed yet" → chose Stage-all→commit→push → committed ALL FOUR files (README.md, docs/guide.md, login.txt, schema.sql). No scoping happened. Root cause: the docs scope phrase is not captured deterministically; the 3B LLM does not scope it. Contrast M-04a (login) which DID scope. Same root cause as M-10c/M-19b/M-20b.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
