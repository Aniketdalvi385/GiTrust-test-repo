# M-17 · --yes cannot undo

| | |
|---|---|
| **LLM** | no |
| **Flagship** | — |
| **Result** | ❌ FAIL (exit 0, not 1 — systemic) |
| **Run date** | 2026-08-04 |

## What this proves

Refusal, exit 1, HEAD untouched.

## Procedure

**Setup:** `mk_sandbox m17`; `echo v2 >> app.txt && git commit -qam "to undo"`.

**Steps:**
```bash
$GITRUST --yes "undo"; echo $?
```

**Expect:** refusal naming the reason (can't auto-choose), exit code **1**, HEAD untouched.

## Result

**❌ FAIL — the refusal is correct and HEAD is safe, but it exits 0 (must be 1), and cites the wrong reason.**

**✅ Refused + HEAD untouched:**
- `gitrust --yes "undo"` **refused** — it did not auto-undo.
- HEAD unchanged: `git rev-parse HEAD` = `5e0c88fbfe3cad97a009d58f94271eeda2b44f5e` = `$PRE`; commit `"to undo"` still present; `git status -sb` → `[ahead 1]`. ✅

**❌ Defect 1 — CRITICAL for this test: exit code 0, must be 1.** `EXIT=0` after the refusal. The suite's defining assertion is *"refusal … exit code **1**."* A refusal that exits 0 signals **success** to any script/CI/`&&` chain — the caller believes the undo happened (or that a no-op was fine) when the tool actually declined to act. **This is the same exit-code dishonesty confirmed in M-08** (paused rebase → exit 0). Two independent paths now → **systemic**: refusals/blocks return `Ok(0)` instead of a nonzero error. Directly violates the exit-code-honesty lens (a not-done op must never return Ok).

**❌ Defect 2 — wrong refusal reason (misapplied copy).** The message was:
> *"--yes flag cannot choose a **reconciliation strategy (rebase vs merge)**. Run interactively and pick a strategy manually."*

But the request was **undo**, which involves no rebase/merge reconcile. The refusal is right in spirit (`--yes` can't auto-pick the undo mode), but it recites the **divergence-reconcile refusal text**, misapplied. Implies the undo-under-`--yes` path falls through to the generic reconcile-refusal branch instead of a dedicated undo refusal — so the user is told to choose a "rebase vs merge strategy" for an op that has neither.

**Root-cause link:** Defect 1 ties M-17 to M-08 as one systemic exit-code bug. Defect 2 is a routing/copy issue (undo refusal not distinguished from reconcile refusal). Watch M-30 (not-a-repo) — another explicit nonzero-exit assertion — to see if the exit-code bug is universal or specific to the AutoConfirm-refusal path.

**Repro:** deterministic.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
