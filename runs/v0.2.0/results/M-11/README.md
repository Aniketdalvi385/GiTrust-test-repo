# M-11 · Mid-rebase never says checkout a branch

| | |
|---|---|
| **LLM** | yes |
| **Flagship** | — |
| **Result** | ✅ PASS |
| **Run date** | 2026-08-04 |

## What this proves

S12 bug stays dead.

## Procedure

**Setup:** reproduce the M-08 conflict pause (mid-rebase): run the M-08 setup, then `$GITRUST "push"` → Rebase → stop at the conflict.

**Steps:**
```bash
$GITRUST "commit my changes"
```

**Expect:** the block names the **rebase** ("A rebase is in progress…") and offers continue/abort. **FAIL instantly if "checkout a branch" appears** — resurrected S12 bug.

## Result

**✅ PASS — the S12 regression stays dead.**

**Setup:** reached the mid-rebase conflict pause (verified `[ahead 1, behind 1]` → rebase → "Paused on conflicts").

**Core assertion:** `gitrust "commit my changes"` while mid-rebase (@ llm · ~11.2s) returned:
> *"A rebase is in progress. Back out with `gitrust "abort rebase"`, or resolve the conflicts and `gitrust "continue rebase"`."*

- **Names the rebase** ✅ ("A rebase is in progress").
- **Offers continue / abort** ✅.
- **The forbidden phrase "checkout a branch" does NOT appear** (grep-verified) — S12 bug is dead. ✅

**Ambient defects (already logged under M-08/M-09, not re-counted here):** the conflict pause still reads *"0 file(s)"* (Defect 1); the stale-snapshot *"interrupted pipeline"* warning fired on the `commit my changes` command (Defect 3). Neither affects the M-11 assertion.

**Repro:** deterministic.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
