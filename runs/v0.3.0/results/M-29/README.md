# M-29 · Ollama down: graceful degrade

| | |
|---|---|
| **LLM** | dash |
| **Ollama** | off |
| **Result** | ⏭️ SKIP (not exercised — Ollama was up) |
| **Run** | v0.3.0 · 2026-08-07 13:31 |

## Notes
The first command showed ◉ (llm · ~15.9s) and SUCCEEDED — meaning Ollama was still RUNNING, so the graceful-degrade path (friendly LLM-down error) was not actually exercised. Not a product failure; the test setup needed Ollama stopped and it wasn't. Re-run with 'brew services stop ollama' to properly verify. (The v0.2 run confirmed graceful degrade PASSES when Ollama is truly down.)

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
