# M-07 · Diverged → merge path

| | |
|---|---|
| **LLM** | yes |
| **Flagship** | — |
| **Result** | ✅ PASS |
| **Run date** | 2026-08-04 |

## What this proves

Merge commit, two parents.

## Procedure

**Setup:** same as M-06 in a fresh sandbox (`mk_sandbox m07; mk_teammate m07; …`).

**Steps:**
```bash
$GITRUST "push"        # choose MERGE
git log -1 --format=%P | wc -w    # expect: 2
```

**Expect:** merge commit created (2 parents); pushed; `0 0`; both changes present.

## Result

**✅ PASS — the merge reconcile path produces a real two-parent merge commit.**

**Divergence confirmed:** `## main...origin/main [ahead 1, behind 1]`.

**Flow:**
1. `gitrust "push"` fetched, detected divergence, raised the **ChoiceGate**; selected **Merge** — consequence sentence: *"Merge — keep both histories, adds a merge commit. Safer if others may have pulled your commits."*
2. 2-step plan (merge → push), snapshot `ff5be0a`.
3. Executed: `Merged origin/main (merge commit recorded)` → `Pushed 2 commit(s) to origin/main` → `✓ Done · on main, ↑0 ↓0`.

**Verified:**
- `git log -1 --format=%P | wc -w` → **`2`** — two parents (the defining assertion). ✅
- `git rev-list --left-right --count origin/main...HEAD` → **`0 0`**.
- Graph shows the merge joining both lines:
  ```
  *   05eebc5 (HEAD -> main, origin/main) Merge origin/main into main
  |\
  | * 9423db1 teammate: hotfix
  * | ff5be0a feat: mine
  |/
  * 30f0fac base
  ```
  Both `app.txt` and `notes.txt` present.

**Minor observations (not failures, same as M-06):** `* (instant)` marker (deterministic reconcile); redundant *"Consider pulling first"* warning shown inside a plan that already merges upstream.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
