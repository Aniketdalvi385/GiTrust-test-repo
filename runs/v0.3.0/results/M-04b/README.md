# M-04b · Scoped feature pipeline — docs scope

| | |
|---|---|
| **LLM** | partial |
| **Ollama** | on |
| **Result** | ⚠️ PASS (with defects) |
| **Run** | v0.3.0 · 2026-08-10 16:22 (router re-run) |

## Notes
ROUTING FIXED (⚡ instant, was ◉ LLM bare-push shipping all 4 files). But scope QUALITY is wrong: only docs/guide.md was Related/pre-checked; README.md — also a docs file — was classified Unrelated/hidden and NOT pushed. A "docs" push that omits the README is under-inclusive. Big improvement over the prior FAIL (no longer ships schema/login), but the resolver missed an obvious docs file. ⚠️ not ✅.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
