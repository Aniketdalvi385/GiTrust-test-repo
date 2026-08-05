# M-23 · Deleted branch → find my lost work ★★

| | |
|---|---|
| **LLM** | no |
| **Flagship** | ★★ |
| **Result** | ✅ PASS (flawless — centerpiece) |
| **Run date** | 2026-08-04 |

## What this proves

Rescue branch at exact oid, HEAD untouched.

## Procedure

**Setup:**
```bash
mk_sandbox m23
git checkout -qb experiment && echo "precious work" > precious.txt && git add . && git commit -qm "the work I'll lose"
LOST=$(git rev-parse HEAD); git checkout -q $BR && git branch -D experiment
HEAD_BEFORE=$(git rev-parse HEAD)
```

**Steps:**
```bash
$GITRUST "find my lost work"   # RecoveryBrowser → pick "the work I'll lose"
git rev-parse rescue/*         # expect == $LOST
git rev-parse HEAD             # expect == $HEAD_BEFORE
```

**Expect:** `rescue/<date>-<oid>` branch created **at exactly `$LOST`**; current HEAD untouched; working tree untouched. **★★ desk-visit automated — record.**

## Result

**✅ PASS — flawless. The ★★ centerpiece ("I lost my work → here it is on a rescue branch") works exactly as designed.**

**Setup:** committed `precious.txt` on `experiment` (`LOST=eb5955bd…`), switched to `main`, deleted `experiment` (`git branch -D` → "Deleted branch experiment (was eb5955b)"), captured `HEAD_BEFORE=c6cdd56f…`. `git log --all` confirmed `experiment` gone from refs.

**All three defining assertions hold:**
1. **Rescue branch at exactly `$LOST`** ✅ — `git rev-parse rescue/20260804-eb5955b` = `eb5955bd58f38e07541f206f278fbb50e93665a6` = `$LOST` (byte-for-byte, verified).
2. **HEAD untouched** ✅ — `git rev-parse HEAD` = `c6cdd56f2d403f45d317a9eb780dec0c6f134cd1` = `$HEAD_BEFORE`. The rescue did not move HEAD.
3. **Working tree untouched** ✅ — `git status -sb` → `## main...origin/main`, still on `main`, clean.

**Experience (the origin story):**
- **Phrase-triggered forensic intent routed correctly** — `"find my lost work"` went straight to the RecoveryBrowser; no fall-through to status (contrast M-10). ✅
- Browser **found the lost commit**: *"just now — 'the work I'll lose' — 1 file"* — human-readable age + subject + file count. ✅
- **Rescue-branch naming exactly per spec:** `rescue/<date>-<oid>` = `rescue/20260804-eb5955b`. ✅
- Success copy accurate + reassuring: *"Recovered eb5955b onto new branch `rescue/20260804-eb5955b`. Your current branch and files are unchanged."* ✅

**Confirms the plan's design insight:** the forensic rescue creates a **ref only** (`create_branch_at`) — it never moves HEAD, never touches index/worktree, never runs a mid-op git verb — so it is **immune to the phantom-op reset bug** (M-16/M-19). Verified against the real oid, not just the success message: the branch genuinely points at `$LOST`. This is the correct, safe recovery design, working.

**Repro:** deterministic (Source A / reflog walk finds the deleted-branch commit).

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).
Recording: see [`recording.md`](recording.md).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
