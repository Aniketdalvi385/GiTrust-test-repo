# M-21 · Failing pre-commit blocks (via system git)

| | |
|---|---|
| **LLM** | yes |
| **Flagship** | — |
| **Result** | ⚠️ PASS (core ✅ / exit 0 defect ❌) |
| **Run date** | 2026-08-04 |

## What this proves

Hook output surfaced, commit blocked.

## Procedure

**Setup:**
```bash
mk_sandbox m21
cat > .git/hooks/pre-commit << 'HOOK'
#!/bin/sh
echo "LINT FAILED"; exit 1
HOOK
chmod +x .git/hooks/pre-commit; echo x >> app.txt
```

**Steps:**
```bash
$GITRUST "commit this"
git rev-list --count HEAD   # unchanged
```

**Expect:** info line that hooks were detected (system git routing); commit **blocked**; hook output ("LINT FAILED") in the failure message; count unchanged.

## Result

**⚠️ PASS on the hook-enforcement assertion; carries the systemic exit-0 defect.**

**Setup:** always-failing `pre-commit` hook (`echo "LINT FAILED"; exit 1`), `app.txt` modified, `BEFORE_COUNT=1`.

**✅ Core assertion — hooks honored, commit blocked, output surfaced:**
- **Hooks detected + system-git routing announced** (both proactively and at exec):
  - Plan warning: *"Hook(s) present (pre-commit) — GiTrust will run them via system git."*
  - At execution: *"hooks detected — using system git so they run."* ✅
- **Commit blocked** — the commit step shows `X … X` (failed); count unchanged (`1` → `1`, verified `git rev-list --count HEAD`). ✅
- **Hook output surfaced** — *"the pre-commit hook refused the operation: LINT FAILED"* — raw `LINT FAILED` shown, not swallowed. ✅
- **`app.txt` remains uncommitted** (`M app.txt`). ✅
- Bonus UX: on failure it preserved a snapshot and offered a *"fix `commit` and continue"* affordance with a "Show — re-print the hook output" option. Reasonable.

**❌ Defect — exit code 0 on a hook-blocked commit.** `EXIT=0`. A commit blocked by a failing hook must exit **nonzero**. **Third confirmed instance of the exit-code bug** (M-08 paused rebase → 0; M-17 refused undo → 0; M-21 hook-blocked commit → 0) ⇒ conclusively **systemic**: every non-success terminal state returns 0. *CI impact, concrete:* `gitrust "commit this" && git push` would proceed to **push despite the commit failing the lint hook** — the exact failure a pre-commit hook exists to prevent.

**Cleaner than the phantom-ops (M-16/M-19):** here the git-layer reporting is **honest** — the commit genuinely did not happen (count unchanged, file still modified). Only the process exit code is wrong. So this is an exit-code-only defect, not a phantom op.

**Note — snapshot left behind** (M-08 lifecycle theme): `~/.gitrust/snapshots/a5c2b596-….json` remained after the blocked commit.

**Repro:** deterministic.

**Cleanup:** `rm ~/.gitrust/snapshots/*.json` before next test.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
