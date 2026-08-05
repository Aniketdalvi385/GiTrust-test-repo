# M-27 · Fail-closed trash-net

| | |
|---|---|
| **LLM** | no |
| **Flagship** | — |
| **Result** | ✅ PASS (fail-closed holds; exit-0 defect) |
| **Run date** | 2026-08-05 |

## What this proves

Refuses on unwritable trash, file survives.

## Procedure

**Setup:**
```bash
mk_sandbox m27
echo untracked > loose.txt
mkdir -p ~/.gitrust/trash && chmod 000 ~/.gitrust/trash
```

**Steps:**
```bash
$GITRUST "clean up my repo"   # choose delete-untracked
echo $?
ls loose.txt                  # still there
chmod 755 ~/.gitrust/trash    # ← CLEANUP, do not skip
```

**Expect:** operation **refuses** (nonzero, error names the backup failure); the untracked file **still exists**. Nothing deleted without a backup. **⚠ Run this test LAST, or restore the chmod immediately — otherwise later trash tests fail-closed.**

## Result

**✅ PASS — fail-CLOSED holds. When the trash backup was impossible, the destructive op refused and deleted nothing. (Systemic exit-0 defect attached.)**

**Setup:** untracked `loose.txt` + `chmod 000 ~/.gitrust/trash` (confirmed `d---------`).

**Defining assertion — fail-closed:**
- Backup attempt **failed** as designed: *"Failed to create trash dir …/20260805-114537 … caused by: Permission denied (os error 13)."*
- Op **refused** — clean step `X … X`, and the **reason names the backup failure** (not a generic error). ✅
- **`loose.txt` SURVIVED, byte-identical** — verified *"SURVIVED, UNCHANGED ✓"*; `git status` still shows `?? loose.txt`. **Nothing deleted without a backup.** ✅

This is the crucial safety guarantee: backup-impossible ⇒ abort **before** deleting. It **holds** — and correctly *errors* rather than *lying* (contrast M-16's false "backup written" claim). Chmod restored to `755` immediately after (verified `drwxr-xr-x`).

**Corroborates the M-26/M-16 diagnosis:** this proves the `clean` path runs `backup_to_trash` as a **hard precondition** of deletion (the backup gates the delete — that's why the failed backup stopped the delete). That's exactly why `clean` is safe (M-26 success, M-27 fail-closed) while `reset` is broken (M-16 phantom): `clean` genuinely invokes the backup; `reset` never executes at all. The three tests together isolate the bug to the reset executor, not the trash subsystem.

**❌ Defect — exit 0 (5th instance).** `EXIT=0` on a safety refusal. Should be nonzero. Fifth confirmation of the systemic exit-code bug (M-08 paused rebase, M-17 refused undo, M-21 hook-blocked commit, M-22 failed revert, M-27 fail-closed refusal). Especially notable here: a script relying on the exit code would believe the cleanup succeeded when it actually (correctly) refused. Not a fail-open (file survived) — so PASS-with-defect, not FAIL.

**Repro:** deterministic.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
