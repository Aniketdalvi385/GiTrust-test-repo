# M-03b · Commit with editable message — "save my changes"

| | |
|---|---|
| **LLM** | llm |
| **Ollama** | on |
| **Result** | ❌ FAIL |
| **Run** | v0.3.0 · 2026-08-10 16:22 (router re-run) |

## Notes
MISROUTE: "save my changes" (◉ LLM) planned only a STAGE step — no commit. Output: "Staged all changes", Done with NO commit; HEAD subject still "base" (unchanged). The user asked to SAVE their changes and nothing was committed. The LLM classified this as a bare add, not add_commit. This is a router-excluded phrasing (commit family is arg-free but routes via LLM here) — candidate for a canonical/router entry. Same class as the other LLM misroutes.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
