# M-02 · LLM-path classification

| | |
|---|---|
| **LLM** | yes |
| **Flagship** | — |
| **Result** | ✅ PASS |
| **Run date** | 2026-07-31 |

## What this proves

Model consulted (◉ marker).

## Procedure

**Setup:** Ollama running (restart it after M-01). Reuse the m01 sandbox or `mk_sandbox m02`.

**Steps:**
```bash
$GITRUST "anything new in my repo?"
```

**Expect:** ◉ marker (model consulted); classified read-only status/log; correct empty-ish summary. Note latency.

## Result

**PASS.** `gitrust "anything new in my repo?"` went through the **model** — marker `@  (llm · ~15.5s)` (vs the `*` fast-path in M-01). Classified the natural-language question as a read-only status and correctly reported the clean tree / up-to-date branch. Exit 0.

**Observations:**
- **Latency ~15.5s** — noticeably slow for a status question; acceptable (correct behavior) but worth tracking as an experience metric.
- **Marker glyph:** binary prints `@` for the LLM path; this README/suite text said `◉`. Cosmetic doc mismatch only — the binary correctly distinguishes model-path (`@`) from fast-path (`*`). Not a failure.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
