# M-04a · Scoped feature pipeline — login scope

| | |
|---|---|
| **LLM** | partial |
| **Ollama** | on |
| **Result** | ⚠️ PASS (with defects) |
| **Run** | v0.3.0 · 2026-08-10 12:13 |

## Notes
Routed through the scoped resolver (⚡). BUT scope quality is wrong: the model pre-checked api_client.txt as Related to login ("might handle authentication"), so the push shipped login.txt + api_client.txt. readme.txt correctly hidden. Scoping MACHINERY works; the model's relatedness judgment is loose. Compare M-04c where the same api_client.txt was called Unrelated — inconsistent relatedness.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
