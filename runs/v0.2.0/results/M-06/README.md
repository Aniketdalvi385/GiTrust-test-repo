# M-06 · Diverged push → rebase → clean ★

| | |
|---|---|
| **LLM** | yes |
| **Flagship** | ★ |
| **Result** | ✅ PASS |
| **Run date** | 2026-08-04 |

## What this proves

Origin-story: rebase then push, 0/0.

## Procedure

**Setup:**
```bash
mk_sandbox m06; mk_teammate m06
echo "my feature" >> app.txt && git commit -qam "feat: mine" && git fetch -q
git status -sb    # confirm: ahead 1, behind 1
```

**Steps:**
```bash
$GITRUST "push"        # ChoiceGate → read both consequence sentences → choose REBASE
git rev-list --left-right --count origin/$BR...HEAD   # expect: 0 0
git log --oneline
```

**Expect:** rebase runs, push completes in the same pipeline; `0 0`; teammate's commit *below* yours; both `app.txt` and `notes.txt` present. **★ Origin story — record it.**

## Result

**✅ PASS — the flagship "origin story" works end-to-end.**

**Divergence confirmed** before the run: `## main...origin/main [ahead 1, behind 1]` (teammate pushed a commit; local had one unpushed commit).

**Flow:**
1. `gitrust "push"` fetched, detected the divergence, and raised a **ChoiceGate** with a plain-English consequence sentence — *"Rebase — replay your 1 commit(s) on top of theirs; history stays linear. Recommended when nobody else has your commits."* No raw git error.
2. Chose rebase → a **2-step plan (rebase → push)** with a snapshot oid.
3. Executed in **one pipeline**: `Successfully rebased and updated refs/heads/main` → `Pushed 1 commit(s) to origin/main` → `✓ Done · on main, ↑0 ↓0`.

**Verified clean:**
- `git rev-list --left-right --count origin/main...HEAD` → **`0 0`** (fully in sync).
- `git log --oneline`:
  ```
  b150b71 (HEAD -> main, origin/main) feat: mine     ← mine, replayed on top
  e83bffb teammate: hotfix                            ← teammate's, below
  3ddf078 base
  ```
  Linear history, teammate's commit below mine, both `app.txt` (mine) and `notes.txt` (teammate) present — nothing lost.

**Minor observations (not failures):**
- Path marker was `* (instant)`, not `@ llm` — divergence reconciliation is deterministic here. Fine, but note the marker semantics differ from a model-classified request.
- The plan showed a warning *"Local branch is 1 commit(s) behind upstream. Consider pulling first…"* **inside a plan that already rebases onto upstream** — redundant/slightly contradictory copy. Cosmetic only; the plan did the right thing.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).
Recording: see [`recording.md`](recording.md).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
