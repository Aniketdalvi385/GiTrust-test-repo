# M-08 · Conflicting rebase → calm pause → continue ★

| | |
|---|---|
| **LLM** | partial |
| **Flagship** | ★ |
| **Result** | ⚠️ PASS (with 3 defects) |
| **Run date** | 2026-08-04 |

## What this proves

Calm handoff, continue verb.

## Procedure

**Setup (the reusable conflict — also used by M-09/M-11):**
```bash
mk_sandbox m08
( cd $TESTROOT/m08 && git clone -q remote.git teammate && cd teammate \
  && git config user.email t@test.com && git config user.name teammate \
  && echo "teammate line1" > app.txt && git commit -qam "teammate: app line1" && git push -q )
# local conflicting edit on the same line:
echo "my line1" > app.txt && git commit -qam "mine: app line1" && git fetch -q
```

**Steps:**
```bash
$GITRUST "push"        # Rebase → conflict expected
echo $?                # nonzero
# then resolve:
echo "resolved line1" > app.txt && git add app.txt
$GITRUST "continue rebase"
```

**Expect:** calm handoff names the conflicted file, says nothing is lost, names `gitrust "continue rebase"` / `gitrust "abort rebase"`; **no** stack-trace. After continue: rebase completes; push if offered; history linear. **★ record.**

## Result

**⚠️ PASS on the core assertion, but with 3 real defects.** (First attempt was invalid — a dropped-parenthesis in the teammate-setup paste moved the shell into the `teammate` clone, so no divergence/conflict was created; re-run below with a verified `[ahead 1, behind 1]` setup.)

**✅ Core assertion holds — calm handoff + continue verb work:**
- Setup verified: `git status -sb` → `[ahead 1, behind 1]` before the push.
- Rebase hit the same-line conflict and **paused calmly**: *"Paused on conflicts in 0 file(s) — nothing is lost. Resolve them, then `gitrust "continue rebase"`, or `gitrust "abort rebase"` to return to where you started."* — names the recovery verbs and reassures nothing is lost.
- `gitrust "continue rebase"` **parsed correctly** (contrast M-04/M-05) and **completed** the rebase: `Successfully rebased and updated refs/heads/main`, linear history:
  ```
  7f4f1a0 (HEAD -> main) mine: app line1        ← replayed on top
  0ca95d7 (origin/main)  teammate: app line1
  c495596 base
  ```
  `app.txt` = `resolved line1`; no rebase left in progress.

**❌ Defect 1 — conflicted-file count wrong AND file not named.** The pause said *"Paused on conflicts in **0 file(s)**"* — there was exactly **1** conflicted file (`app.txt`). Count is wrong (shows 0), and the suite's expectation that the message **names the conflicted file** is unmet — it names none. Same "count/argument dropped" family as M-04/M-05. *User impact:* the calm message loses its single most useful datum (which file to fix).

**❌ Defect 2 — exit-code dishonesty: paused rebase returns 0.** `echo $?` immediately after the pause printed **`0`**. A conflict pause is **not success** and must exit nonzero (plan-review exit-code lens: a not-done/paused op must never return Ok). Also, raw git noise leaked above the calm message — the `CONFLICT (content):` line and the full `hint: … git rebase --continue/--skip/--abort` block printed to the terminal, partially defeating the "no raw git panic" goal (the calm message is there, but it's stacked on top of the raw dump).

**❌ Defect 3 — stale snapshot not cleared → spurious "interrupted pipeline" warning.** On `continue rebase`, it warned: *"⚠ An interrupted pipeline was found (captured 2026-08-04T16:02:01…). Run 'gitrust --recover'…"*. The pause left a snapshot that the continue did not clean up. Confirmed leftover: `~/.gitrust/snapshots/62cf4feb-….json` still on disk after a fully-completed rebase. *User impact:* every subsequent command nags about an interrupted pipeline that is actually finished — and points the user at `--recover`, which could undo their just-completed work. **Cleanup needed before later tests** (see note).

**Cleanup performed for test hygiene:** the stale snapshot must be removed so it doesn't pollute M-09+ (`rm ~/.gitrust/snapshots/*.json`).

**Repro:** deterministic (setup produces a guaranteed same-line conflict).

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).
Recording: see [`recording.md`](recording.md).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
