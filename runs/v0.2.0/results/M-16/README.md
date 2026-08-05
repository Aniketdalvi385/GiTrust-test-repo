# M-16 · Undo → discard: TypeToConfirm + trash-net

| | |
|---|---|
| **LLM** | no |
| **Flagship** | — |
| **Result** | ❌ FAIL (CRITICAL — phantom op + false backup) |
| **Run date** | 2026-08-04 |

## What this proves

Trash backup written, content matches.

## Procedure

**Setup:** as M-15 (fresh `mk_sandbox m16` + the commit); note the modified file content.

**Steps:**
```bash
$GITRUST "undo"        # choose DISCARD COMPLETELY → TypeToConfirm
ls ~/.gitrust/trash/   # new timestamped dir
```

**Expect:** TypeToConfirm gate before anything happens; success line names the trash backup ("…in ~/.gitrust/trash/<ts>/ for 7 days"); backed-up file content matches what you noted (`diff`).

## Result

**❌ FAIL — CRITICAL. The discard reported success but performed NEITHER the reset NOR the backup. A destructive op claimed a safety net that does not exist.**

**✅ What worked (the gate front-end):**
- The four-option undo Select gate rendered all four options (screenshot evidence): *Keep them staged / Keep them in files / Make an inverse commit (revert) / **Discard completely***. (This also **corrects M-15** — the four options ARE present; M-15's earlier "missing gate" note was the collapsed post-selection view.)
- Choosing **Discard completely** raised a proper **TypeToConfirm** gate with a full destructive warning, requiring the user to type `4b472b8` before proceeding. ✅

**❌ Defect 1 — CRITICAL: false backup claim (trash-net fail-OPEN).** The success line stated:
> *"A backup of the discarded changes is in /Users/aniket.dalvi/.gitrust/trash for 7 days."*

But **`~/.gitrust/trash/` does not exist** — `ls ~/.gitrust/trash/` → *"No such file or directory"*, and `ls ~/.gitrust/` shows only a `snapshots/` dir, no `trash/`. **No backup was ever written.** This is the exact opposite of the Phase 14 **fail-CLOSED** invariant (backup must be written *before* the destructive git call, or the op aborts). Here the tool printed the backup-success copy unconditionally, promising a recovery path that isn't there. Most dangerous failure class: a safety net that lies about its own existence.

**❌ Defect 2 — CRITICAL: the destructive op silently no-op'd.** The pipeline reported `→ reset (hard)` and `✓ Done`, but **nothing was reset**:
- `git log` → HEAD **still at `4b472b8 "feat: the mistake"`** (commit NOT dropped).
- Working tree clean; `app.txt` still contains `precious content v2`.
- `git status -sb` → `## main...origin/main [ahead 1]` (still ahead — the commit is intact).

So a `reset --hard` was reported as executed while HEAD did not move. An operation reporting success while doing nothing is a severe correctness failure. (Ironically, this no-op is the *only* reason no data was lost — but the tool cannot rely on its own destructive step failing to be safe.)

**❌ Defect 3 — copy bug in TypeToConfirm.** The safety line reads *"This op requires you to type the **branch name** to confirm."* but the prompt actually asks to type the **commit oid** (`4b472b8`). Branch-vs-commit copy mismatch.

**Root-cause hypothesis (single bug likely explains Defects 1 & 2):** if the trash backup is meant to run *inside* `Git2Operations::reset(Hard)` and fail-closed, a bug in that method could cause it to (a) skip creating the trash dir AND (b) skip/short-circuit the actual git reset, while the pipeline still prints its canned `reset (hard)` + backup-success strings from the step metadata rather than from real outcomes. i.e. **the success copy is decoupled from whether the op actually ran.** That decoupling is the thing to fix: outcomes must be reported from real results, and the backup must be a hard precondition of the reset.

**Trash-net verification could not run** (no trash dir to diff against) — the byte-identical assertion is moot because the backup never existed.

**Severity: CRITICAL.** This is the single most important finding of the run: the destructive-safety subsystem is fundamentally not doing its job, and it actively misinforms the user.

**⚠️ UPDATE after M-26 — root cause narrowed to the RESET path, not the trash module.** M-26 (`clean`) later wrote a **real, byte-identical, nested trash backup** and really deleted the files — proving the **trash-net module itself is sound**. And M-19 showed `reset --soft` also no-op'd. So the failure here is **not** the trash-net: it's that the **`reset` execution path reports success without running the git reset**, which means its in-method `backup_to_trash` never fires either. Both symptoms (no reset + no backup) stem from one bug: the reset executor emits its success/backup copy from step metadata instead of from a real, verified git mutation. **Fix target: the reset executor seam** (`Git2Operations::reset` for both Hard and Soft), not `trash.rs`. M-26 is the control proving the module works when actually invoked.

**Repro:** deterministic.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
