# M-04a · Scoped feature pipeline — login scope

| | |
|---|---|
| **LLM** | partial |
| **Ollama** | on |
| **Result** | ⚠️ PASS (with defects) |
| **Run** | v0.3.0 · 2026-08-10 16:22 (router re-run) |

## Notes
⚡ instant (fast-path scoped — routing FIXED). Resolver quality loose: pre-checked login.txt + api_client.txt as Related to login ("might handle authentication"); auth.txt offered as Uncertain and toggled on. Pushed login.txt + api_client.txt + auth.txt. readme.txt correctly excluded. Routing is now instant and correct; the model relatedness is over-inclusive (api_client pulled into "login").

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
