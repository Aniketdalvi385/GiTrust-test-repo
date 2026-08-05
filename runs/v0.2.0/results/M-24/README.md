# M-24 · Dropped stash surfaces

| | |
|---|---|
| **LLM** | no |
| **Flagship** | — |
| **Result** | ✅ PASS (proves Source B / odb scan) |
| **Run date** | 2026-08-04 |

## What this proves

Stash-shaped candidate recovered.

## Procedure

**Setup:** `mk_sandbox m24`; `echo wip >> app.txt; git stash push -m "important wip"; git stash drop`.

**Steps:**
```bash
$GITRUST "find my lost work"
```

**Expect:** the browser lists a **stash-shaped** candidate (WIP message); restoring it creates a rescue branch containing the wip change.

## Result

**✅ PASS — dropped stash surfaced and recovered byte-perfectly. Proves Source B (the odb scan) is real and wired in.**

**Setup:** `echo wip >> app.txt` → `git stash push -m "important wip"` → `git stash drop` (git reported `Dropped refs/stash@{0} (b98c90ff4ac2757…)`). Confirmed truly gone: `git stash list` **empty**, tree clean, **no reflog trace**. `HEAD_BEFORE=ec0655c…`.

**Core assertion:**
- The RecoveryBrowser **surfaced the dropped stash**: *"just now — 'On main: important wip' — 1 file **[stash]**"* — the **`[stash]` tag** = the plan's `is_stash_shaped` flag working. ✅
- Restored → `rescue/20260804-b98c90f`; **`git show rescue/…:app.txt`** contains the `wip` line — actual dropped content recovered. ✅
- **Recovered oid = dropped-stash oid, verified:** `git rev-parse rescue/20260804-b98c90f` = `b98c90ff4ac2757f1a230a028fe3258f1d4ce1ce` = exactly the oid git printed on `stash drop`. Stash topology intact (`On main: important wip` over `index on main: … base`). ✅
- **HEAD untouched:** `git rev-parse HEAD` = `ec0655c…` = `$HEAD_BEFORE`; clean tree, still on `main`. ✅

**Why this is significant (the two-source design proof):** a dropped stash leaves **no reflog trace**, so Source A (reflog walk — which carried M-23's deleted branch) **cannot** find it. Only the **bounded odb scan (Source B)** can. A reflog-only implementation would have **failed M-24 with "nothing found."** It found it, correctly tagged it `[stash]`, and recovered the exact content — so Source B is genuinely implemented and working. M-23 (Source A) ∧ M-24 (Source B) together validate the whole two-source recovery architecture.

**Trash-net not involved** (recovery is non-destructive), so M-16's trash-net breakage does not affect this path.

**Repro:** deterministic.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
