# M-26 · Clean-up gate + trash backup, nested dirs

| | |
|---|---|
| **LLM** | no |
| **Flagship** | — |
| **Result** | ✅ PASS (trash-net works for `clean`) |
| **Run date** | 2026-08-05 |

## What this proves

Nested untracked dir backed up identically.

## Procedure

**Setup:**
```bash
mk_sandbox m26
echo mod >> app.txt                                   # tracked change
mkdir -p junk/inner && echo tmp > junk/inner/file.txt # nested untracked
```

**Steps:**
```bash
$GITRUST "clean up my repo"    # gate must state tracked/untracked COUNTS + name trash-net → choose delete-untracked
ls ~/.gitrust/trash/*/junk/inner/file.txt
diff junk/inner/file.txt <(cat ~/.gitrust/trash/*/junk/inner/file.txt)  # (junk/ is gone; compare the backup)
```

**Expect:** `junk/` gone; `~/.gitrust/trash/<ts>/junk/inner/file.txt` exists and `diff`s identical (the nested-dir hole, verified by hand); the tracked modification untouched.

## Result

**✅ PASS — the clean-up gate AND the trash-net both work end-to-end, including the nested-untracked-dir case. Outcome #3 (correct).**

**Setup:** tracked mod (`M app.txt`) + nested untracked dir (`junk/inner/file.txt`); expected content captured.

**Gate (destructive-phrase) — correct:**
- `gitrust "clean up my repo"` raised a gate stating the **count + consequence**: *"Delete untracked files — delete **1 untracked file(s)** — these have NO git history; only the trash-net protects them."* Names the trash-net before acting. ✅
- Danger marker `⛔` on the clean step (untracked deletion graded severe, per plan's danger.rs grading).

**Execution — real, not phantom:**
- `junk/` **actually deleted**: *"Removing junk/"*, verified `ls junk` → deleted. ✅
- **Trash dir created**: `~/.gitrust/trash/20260805-113833/` — timestamp **colon-free `YYYYMMDD-HHMMSS`** (Windows-safe, exactly per plan). ✅
- **Nested backup byte-identical**: `~/.gitrust/trash/20260805-113833/junk/inner/file.txt` exists; `diff` vs expected → **BYTE-IDENTICAL ✓**. Full nested path preserved (`find` shows `…/junk/inner/file.txt`). **The nested-untracked-dir fail-open hole the plan called out is CLOSED** — recurse-untracked-dirs + recursive copy both work. ✅
- **Tracked change untouched**: `app.txt` still `M` (modified), not reverted — clean scoped to untracked only. ✅

**🔑 CRITICAL cross-test insight — the trash-net is NOT uniformly broken.** M-26 (`clean`) writes a real, byte-identical, nested backup and really deletes. M-16 (`reset --hard`) claimed a backup that never existed and no-op'd the reset; M-19 (`reset --soft`) also no-op'd. → **The bug is NOT the trash-net module** — it works when actually invoked (proven here). **The bug is the RESET execution path specifically:** `reset` reports success from step metadata without running the git reset, so its in-method `backup_to_trash` never fires either. `clean` invokes `backup_to_trash` then really deletes, so both work. This **sharpens the M-16/M-19 diagnosis decisively**: fix the reset executor seam, not the trash module. (See M-16 for the phantom-op writeup; M-26 is the control that proves the module is sound.)

**Exit code:** `EXIT=0` — correct (op succeeded).

**Repro:** deterministic.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
