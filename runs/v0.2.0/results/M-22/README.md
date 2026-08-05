# M-22 · Revert parity: succeeds despite the same hook

| | |
|---|---|
| **LLM** | no |
| **Flagship** | — |
| **Result** | ✅ PASS (on clean re-run) |
| **Run date** | 2026-08-04 |

## What this proves

Revert succeeds (no pre-commit).

## Procedure

**Setup:** keep M-21's failing hook; ensure there's a commit to revert (the base commit works).

**Steps:**
```bash
$GITRUST "revert last commit"
```

**Expect:** the revert **succeeds** (inverse commit exists) — matching real git, where revert doesn't run pre-commit. The asymmetry with M-21 is intentional; both passing together is the parity proof.

## Result

**⏳ Parity assertion NOT yet fairly tested — first run was invalid (dirty working tree). Re-run on a clean tree pending.** Two real defects surfaced anyway (recorded below).

**Why run 1 was invalid:** cleanup of M-21's residue was insufficient — after `git checkout -- app.txt; git reset`, `git status -sb` still showed ` M app.txt` (a leftover working-tree modification). The revert therefore ran against a **dirty tree that conflicts with the revert**, and git correctly refused:
> *"Your local changes to app.txt would be overwritten by merge. Please commit your changes or stash them before you merge. Aborting / fatal: revert failed"*

This is **correct git behavior** (can't revert onto a conflicting dirty tree), so the revert-succeeds-despite-hook parity claim was **not exercised**. Re-running in a fresh `m22` sandbox with the hook re-installed and a verified-clean tree.

**Defect 1 — exit-code bug, 4th confirmation.** The revert **failed** (`X revert X`, *"fatal: revert failed"*, *"exited with status exit status: 128"*) yet **`EXIT=0`**. A failed git op reported as success. Joins M-08 (paused rebase), M-17 (refused undo), M-21 (hook-blocked commit) → **four independent paths now return 0 on non-success. Systemic, ironclad.**

**Defect 2 — no pre-flight dirty-tree guard before revert.** The tool attempted the revert on a dirty tree and let **raw git fail with status 128**, surfacing the raw git error, instead of pre-checking ("working tree has conflicting changes — stash or commit first") the way it *does* pre-check commits (cf. M-20's "Nothing staged" pre-check). A calm guard would be more consistent than leaking `git revert … exited with status 128`. Minor relative to the exit code, but a real UX gap.

*(Verified after run 1: count still `1`, no Revert commit, `a92ab72 base` still at tip — the revert genuinely did nothing, consistent with the honest git-layer reporting; only the exit code lied.)*

**Re-run result — ✅ PASS.** Fresh `m22` sandbox, hook re-installed, tree verified clean (`## main...origin/main`, no dirty file), `BEFORE_COUNT=1`:
- `gitrust "revert last commit"` **succeeded despite the failing pre-commit hook**: `[main 9a91c9c] Revert "base"` → *"→ Reverted 8daac11 (inverse commit added)"*.
- Count **+1** (`1` → `2`, verified). Inverse commit at tip: `9a91c9c Revert "base"` above `8daac11 base`. ✅
- `git status -sb` → `[ahead 1]` (the new inverse commit).

**Parity proof complete (M-21 ∧ M-22):** with the *same* failing `pre-commit` hook, the **commit is blocked (M-21)** but the **revert succeeds (M-22)** — the intended asymmetry. GiTrust routes revert as a genuine `git revert` (which does not run pre-commit), not as a commit. ✅

**Confirms a root-cause boundary:** revert is **NOT** affected by the phantom-op reset bug (M-16/M-19). Here the mutation genuinely happened (count changed, real commit created), so the phantom-op defect is **specific to the reset execution path**, not all mutating ops.

**Exit code:** `EXIT=0` — **correct here**, because the op succeeded. (The systemic exit-0 bug manifests only on failure/refusal/block paths; a successful revert legitimately returns 0. Run 1's exit-0 was a defect because that revert *failed*; this run's is fine.)

**Repro:** deterministic on a clean tree.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
