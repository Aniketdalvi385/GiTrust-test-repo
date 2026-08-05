# M-18 · Multi-count undo halts with guidance

| | |
|---|---|
| **LLM** | yes |
| **Flagship** | — |
| **Result** | ✅ PASS |
| **Run date** | 2026-08-04 |

## What this proves

No action, guidance only.

## Procedure

**Setup:** `mk_sandbox m18`; make **three** commits in a row.

**Steps:**
```bash
$GITRUST "undo the last 3 commits"
```

**Expect:** no gate, no action — guidance offering `squash last 3` / revert-specific / undo-most-recent; HEAD unchanged. The LLM-extracted count must never act.

## Result

**✅ PASS — multi-count undo halts with guidance and never acts on the count.**

**Setup:** three commits (`commit 1/2/3`); `PRE = 4e3beeb…`.

**Core assertion:**
- `gitrust "undo the last 3 commits"` (@ llm · ~16.7s) **halted with guidance, no gate, no action**:
  > *"Multi-commit undo isn't supported yet. Did you mean: squash the last 3 into one (`gitrust "squash last 3"`), revert a specific commit, or undo just the most recent (`gitrust "undo"`)?"*
- Offers all three suggested alternatives (squash-3 / revert-specific / undo-most-recent). ✅
- **HEAD unchanged:** `git rev-parse HEAD` = `4e3beeb…` = `$PRE`; all three commits still present. ✅
- **The LLM-extracted count "3" never acted** — the defining safety assertion. ✅

**Notable — sharpens the argument-drop diagnosis (M-04/05/10):** this is the **first argument-carrying request handled correctly.** The LLM *did* extract the count (echoed "the last 3" / "squash last 3"), and the tool used it to **decline + guide** rather than act. So the extraction plumbing works; the failures elsewhere are specifically in the **act-on-extracted-target** path. "Recognize but don't act" = reliable; "recognize and act on the target" = broken. Useful boundary for the fix.

**Exit-code note:** this halt exited 0. Arguably acceptable here (guidance for an unsupported op, not a refusal of a valid op like M-17), but noting it for the exit-code consistency review — a reasonable argument exists that "unsupported request" should also be nonzero.

**Repro:** LLM-path but behavior consistent; count-extraction was correct this run.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
