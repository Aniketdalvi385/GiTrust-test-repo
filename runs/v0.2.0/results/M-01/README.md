# M-01 · Fast-path status (Ollama off)

| | |
|---|---|
| **LLM** | no |
| **Flagship** | — |
| **Result** | ✅ PASS |
| **Run date** | 2026-07-31 |

## What this proves

Fast path bypasses the model.

## Procedure

**Setup:** `mk_sandbox m01`; then **stop Ollama** (quit the app or `pkill ollama`).

**Steps:**
```bash
$GITRUST "status"
```

**Expect:** instant response with the ⚡ fast-path marker — no model call, no error about Ollama. **Restart Ollama after.**

## Result

**PASS.** With Ollama killed (`pkill ollama`), `gitrust "status"` returned **instantly** with the fast-path marker `*  (instant)` — full status render (branch/tracking/last commit/clean tree/last-fetch note) and **no error about Ollama being down**. The fast path bypasses the model entirely, as designed. Exit 0.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
