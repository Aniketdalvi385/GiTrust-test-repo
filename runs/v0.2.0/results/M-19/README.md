# M-19 · Squash last 3: tree-identical

| | |
|---|---|
| **LLM** | yes |
| **Flagship** | — |
| **Result** | ❌ FAIL (wrong op + phantom no-op) |
| **Run date** | 2026-08-04 |

## What this proves

Count -2, tree oid identical.

## Procedure

**Setup:**
```bash
mk_sandbox m19
# three commits editing DIFFERENT files:
echo a > a.txt && git add a.txt && git commit -qm c1
echo b > b.txt && git add b.txt && git commit -qm c2
echo c > c.txt && git add c.txt && git commit -qm c3
TIP_TREE=$(git rev-parse HEAD^{tree})
```

**Steps:**
```bash
$GITRUST "squash the last 3 commits"   # confirm, edit the message
git rev-list --count HEAD
git rev-parse HEAD^{tree}               # expect == $TIP_TREE
```

**Expect:** count dropped by 2; tree oid equals `$TIP_TREE` (identical content, one commit).

## Result

**❌ FAIL — the squash did not happen. It planned the wrong (single-commit) op, then that op was a phantom no-op.**

**Setup:** three commits touching different files (`c1`/`c2`/`c3`); `TIP_TREE = bf23f090…`; `BEFORE_COUNT = 4`.

**The numbers show nothing changed:**
- Commit count **`4` → `4`** — expected `2` (drop by 2 for a 3→1 squash). **No commits collapsed.** ❌
- `git log` **identical** before and after: `c3 / c2 / c1 / base` all still separate.
- `HEAD^{tree}` = `bf23f090…` = `$TIP_TREE` — matches, but **trivially**: a no-op preserves the tree. The "tree-identical" assertion is technically satisfied yet **meaningless** here, because no squash occurred to test it.

**Defect A — wrong operation: "squash the last 3" was interpreted as a single-commit soft reset.** The plan preview read *"Reset --soft preview: Will move HEAD back from 2b3f99f c3 … Files: kept staged"* — a **1-commit** soft reset, not `reset --soft HEAD~3`. The count "3" was effectively dropped (argument-drop pattern, now hitting an **action** — exactly the M-04/05/10 failure mode applied to a mutating op). Worse, the plan had **only a `reset` step and no re-commit / no message-edit prompt** — a squash must end in one new commit, so even a correct 3-commit soft reset would have left 3 staged files and no squash commit. The squash *pipeline* is not implemented as a squash at all here.

**Defect B — phantom no-op (execution decoupled from reporting).** It reported `→ reset (soft)` and `✓ Done · ↑3 ↓0`, but **HEAD did not move and nothing was staged**: verified `git log` HEAD still `2b3f99f c3`, count `4`, `git status --porcelain` **empty** (clean tree, nothing staged). So even the single-commit soft reset it planned **did not execute** — success was printed for an operation that had no effect. **This is the second confirmed "reset reported done but no-op'd"** (M-16 was `reset --hard`; this is `reset --soft`).

**Cross-test root-cause signal (important):** M-16 (`reset --hard`) and M-19 (`reset --soft`) **both** report success while HEAD stays put. → the **`Git2Operations` reset execution path is broken for both hard and soft modes** — the reset git call is not actually moving HEAD (or is being skipped), while the pipeline prints its canned success line from step metadata. Combined with M-16's phantom trash backup, the evidence points to a **reset/executor seam that emits success copy without performing (or verifying) the underlying git mutation.** High-priority single root cause likely explaining M-16 + M-19.

**Defect C — snapshot left behind** (M-08 lifecycle issue): `~/.gitrust/snapshots/` non-empty after this op.

**Repro:** deterministic (setup + the reset no-op are not model-variance; the LLM parse of "squash 3"→soft-reset-1 may vary, but the no-op execution is structural).

**Cleanup:** `rm ~/.gitrust/snapshots/*.json` before next test.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
