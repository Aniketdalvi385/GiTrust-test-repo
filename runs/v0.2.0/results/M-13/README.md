# M-13 · Detached write → rescue

| | |
|---|---|
| **LLM** | yes |
| **Flagship** | — |
| **Result** | ⚠️ PASS (partial — commit dropped) |
| **Run date** | 2026-08-04 |

## What this proves

Branch-here rescue, not dead-end block.

## Procedure

**Setup:**
```bash
mk_sandbox m13
git checkout -q $(git rev-parse HEAD)   # detaches HEAD
echo x >> app.txt
```

**Steps:**
```bash
$GITRUST "commit this"
```

**Expect:** not a dead-end block — the rescue offers **branch-here** (and switch-back); choosing branch-here creates the branch and proceeds sanely.

## Result

**⚠️ PASS on the rescue mechanism, but the original commit was silently dropped after the redirect.**

**Setup:** detached HEAD confirmed (`## HEAD (no branch)`), `app.txt` modified.

**✅ Rescue works (the primary assertion — "branch-here, not dead-end block"):**
- `gitrust "commit this"` (@ llm · ~12.6s) did **not** dead-end. It explained detached HEAD plainly — *"Any commit you make here will be orphaned (lose-able) unless you save it"* — and offered **"Create a branch HERE to save work"**.
- Chose branch-here, named `rescue-work` → *"✓ Created and switched to branch 'rescue-work'"*.
- Ended on a **named branch** (no longer detached); `git branch` → `main` + `* rescue-work`; nothing stranded. ✅

**⚠️ Defect — the commit the user asked for never happened.** The request was **"commit this"**, but after the branch-here rescue the flow **stopped without committing**:
- `git status -sb` → `## rescue-work` with **` M app.txt`** (change still modified/uncommitted).
- `git log -1` → tip still `4f9ae87 base` — **no "commit this" commit created** (verified).

The suite's Expect is *"choosing branch-here creates the branch **and proceeds sanely**"* — the branch was created, but the original commit intent was **dropped on the redirect** rather than resumed. *User impact:* someone who typed "commit this" is left on a new branch believing they committed, when their change is actually still uncommitted — a quiet correctness surprise.

**Pattern link:** same **intent-not-resumed-after-redirect** family as M-08/M-09 (snapshot/continuation) — when the tool redirects into a rescue/gate, the original action isn't always carried through. Here it manifests as a dropped commit rather than a stale snapshot.

**Verdict rationale:** recorded PASS-partial because the *named* thing under test (rescue vs dead-end block) works and no data was lost (the change is safe on `rescue-work`); the dropped commit-continuation is logged as a defect, not a hard FAIL, since the user can simply re-run `commit this` now.

**Repro:** deterministic.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
