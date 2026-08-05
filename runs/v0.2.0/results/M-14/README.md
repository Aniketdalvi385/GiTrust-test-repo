# M-14 · Stranded-commit guard ★

| | |
|---|---|
| **LLM** | no |
| **Flagship** | ★ |
| **Result** | ✅ PASS |
| **Run date** | 2026-08-04 |

## What this proves

Branch-here offered first, nothing stranded.

## Procedure

**Setup:**
```bash
mk_sandbox m14
git checkout -q $(git rev-parse HEAD)   # detach
echo y >> app.txt && git commit -qam "detached work"   # commit WHILE detached
```

**Steps:**
```bash
$GITRUST "checkout $BR"
```

**Expect:** the guard refuses the naive switch-away and offers branch-here **first**, warning commits would be stranded; branch-here preserves the commit on a new branch; nothing lost. **★ record.**

## Result

**✅ PASS — the stranded-commit guard works exactly as designed. Safety centerpiece confirmed.**

**Setup:** detached at `b177cb6 "detached work"` — a real commit on no branch (verified via `git log`/`status`).

**Core assertion:**
- `gitrust "checkout main"` (@ llm · ~16.7s) triggered the guard (did **not** naively switch, did **not** dead-end block).
- Guard warning is precise: *"You have **1 commit(s) here that are on NO branch** — switching away now would **strand** them."* — names the exact count and consequence. ✅
- Offered **branch-here first** → chose it → `saved-work` created and switched to.

**Nothing stranded — verified:**
- `git branch` → `main` + `* saved-work`.
- `git log --oneline -2` → **`b177cb6 (HEAD -> saved-work) detached work`** — the previously-detached commit is now safely reachable on `saved-work`. ✅
- Clean status on the new branch.

**Contrast with M-13 (why this one is clean, not partial):** here the user's request was to **leave** (checkout). The guard correctly *replaces* the leave with the rescue — there is no original action to resume, so nothing is dropped. M-13 dropped a *commit* because the request was to commit; M-14's request was to switch, which is exactly what should be refused. Correct design.

**Consistency observation (not a failure) — links to M-05:** the identical phrase `"checkout main"` **failed to parse in M-05** ("No target branch specified"), but here routed correctly. Difference: M-14's detached-HEAD situation intercepts via the situation-gate path *before* the plain-checkout parse runs, so the M-05 parse bug is bypassed. This localizes the M-05 defect to the **plain (no-situation) checkout parse path**, not the situation-gate path — useful for the fix.

**Repro:** deterministic (guard is situation-driven, not model-dependent for the trigger).

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).
Recording: see [`recording.md`](recording.md).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
