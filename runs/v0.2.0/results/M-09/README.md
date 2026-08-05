# M-09 · Abort restores exactly

| | |
|---|---|
| **LLM** | no |
| **Flagship** | — |
| **Result** | ⚠️ PASS (recurring defects) |
| **Run date** | 2026-08-04 |

## What this proves

HEAD returns to exact pre-rebase tip.

## Procedure

**Setup:** reproduce the M-08 conflict state, but capture the tip **before** invoking gitrust:
```bash
# (run the M-08 setup block first)
PRE=$(git rev-parse HEAD)
$GITRUST "push"        # Rebase → conflict (leaves mid-rebase)
```

**Steps:**
```bash
$GITRUST "abort rebase"
git rev-parse HEAD     # expect == $PRE
$GITRUST "status"      # no rebase language
```

**Expect:** HEAD returns to exactly `$PRE`; working tree clean; situation normal.

## Result

**⚠️ PASS on the defining assertion; carries the same M-08 defects (now confirmed as a pattern).**

**✅ Core assertion — exact restoration:**
- `PRE = 29f6b5190a73e3849e1f7d61a03bd4b12fdce42b` (captured before the rebase).
- After `gitrust "abort rebase"`: `git rev-parse HEAD` = `29f6b5190a73e3849e1f7d61a03bd4b12fdce42b` — **byte-for-byte equal to PRE.** ✅
- `abort rebase` parsed + ran: *"Rebase aborted — back to the original HEAD"*.
- Working tree clean; no `.git/rebase-merge` / `rebase-apply` left (verified); `[ahead 1, behind 1]` correctly restored (that was the pre-rebase state).
- Final `gitrust "status"` reads normal — *"Diverged from upstream (1 ahead, 1 behind). Pull first"* — **no rebase/conflict language**. ✅
- `✓ Done · ↑1 ↓1` correctly reflects the restored diverged counts.

**❌ Defect 1 recurs (conflicted-file count).** Pause again said *"conflicts in **0 file(s)**"* — should be 1 (`app.txt`), and the file is not named. Same as M-08 → confirms it's systemic, not a fluke.

**❌ Defect 3 recurs and is broader — abort also fails to clear the snapshot, and the warning now leaks into read-only `status`.** The *"⚠ An interrupted pipeline was found … Run 'gitrust --recover'"* warning fired on **both** `abort rebase` **and** the subsequent `gitrust "status"`. Confirmed leftover on disk after a clean abort: `~/.gitrust/snapshots/51283a74-….json`. So **neither continue (M-08) nor abort (M-09) clears the pause snapshot.** *User impact, elevated:* after a clean abort the tool nags on every command — including plain status — and points at `--recover`, which would try to "restore" a repo that is already correctly restored. Actively misleading.

**Cleanup for test hygiene:** `rm ~/.gitrust/snapshots/*.json` again before the next test.

**Repro:** deterministic.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
