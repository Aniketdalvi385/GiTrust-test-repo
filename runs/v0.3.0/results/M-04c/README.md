# M-04c · Scoped feature pipeline — api scope

| | |
|---|---|
| **LLM** | partial |
| **Ollama** | on |
| **Result** | ⚠️ PASS (with defects) |
| **Run** | v0.3.0 · 2026-08-10 12:13 |

## Notes
Routed through the scoped resolver (◉). Scope quality wrong the OTHER way: api_client.txt (the obvious api file) was classified Unrelated/hidden; only api_routes.txt was offered (as Uncertain). Pushed api_routes.txt only — api_client.txt, the primary api file, was EXCLUDED. Machinery works; model relatedness is unreliable and inconsistent with M-04a (which called api_client.txt related-to-login).

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
