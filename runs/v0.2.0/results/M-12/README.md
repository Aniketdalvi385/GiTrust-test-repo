# M-12 · Merge-aware commit: two parents

| | |
|---|---|
| **LLM** | yes |
| **Flagship** | — |
| **Result** | ✅ PASS (1 cosmetic note) |
| **Run date** | 2026-08-04 |

## What this proves

Silent-merge-destruction bug stays dead.

## Procedure

**Setup:**
```bash
mk_sandbox m12
git checkout -qb side && echo A > app.txt && git commit -qam side
git checkout -q $BR && echo B > app.txt && git commit -qam mainline
git merge side   # conflicts
echo RESOLVED > app.txt && git add app.txt   # resolved, NOT committed — MERGE_HEAD present
```

**Steps:**
```bash
$GITRUST "commit the merge"
git log -1 --format=%P | wc -w   # expect: 2
git status                        # no merge language
```

**Expect:** commit succeeds with **exactly 2 parents**; merge state cleaned. Two parents is the whole test.

## Result

**✅ PASS — merge-aware commit records two parents; silent-merge-destruction bug stays dead.**

**Setup:** in-progress merge with `MERGE_HEAD` present (verified), conflict resolved but not committed.

**Core assertion:**
- `gitrust "commit the merge"` (@ llm · ~10.0s) drafted `Merge branch 'side'` and committed (695ec3b→0f609e8).
- **`git log -1 --format=%P | wc -w` → `2`** — exactly two parents. ✅ Second parent NOT dropped.
- Merge state cleaned: `MERGE_HEAD` gone (verified), `git status` → "nothing to commit, working tree clean", no merge language.
- Graph confirms the merge topology:
  ```
  *   0f609e8 (HEAD -> main) Merge branch 'side'
  |\
  | * c297269 (side) side
  * | 695ec3b mainline
  |/
  * 4ad3b6a (origin/main) base
  ```

**Root-cause boundary confirmed:** this is a **target-carrying phrase** ("commit *the merge*") that **passed** — because the merge state is on disk (`MERGE_HEAD`), so git supplies the second parent regardless of phrase parsing. This sharpens the argument-drop diagnosis (M-04/05/10): the pattern only bites when the tool must **extract** the target from the phrase; when the needed state is already on disk, the action succeeds.

**Cosmetic note (not a failure):** the recorded commit message literally retained the `# Conflicts:` comment block:
```
Merge branch 'side'

# Conflicts:
#	app.txt
```
git's normal commit-message cleanup strips `#` comment lines; GiTrust committed the raw drafted message without that cleanup pass, so the comments persisted into history. Minor polish item.

**Repro:** deterministic.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
