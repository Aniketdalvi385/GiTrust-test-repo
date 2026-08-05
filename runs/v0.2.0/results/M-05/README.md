# M-05 · Branch create + dirty-switch block

| | |
|---|---|
| **LLM** | no |
| **Flagship** | — |
| **Result** | ❌ FAIL |
| **Run date** | 2026-07-31 |

## What this proves

Dirty switch blocked, not crash.

## Procedure

**Setup:** `mk_sandbox m05`.

**Steps:**
```bash
$GITRUST "create branch feature-x"
echo x >> app.txt
$GITRUST "checkout $BR"
```

**Expect:** branch created + confirmed; the dirty switch is **blocked with a clear message** (auto-stash SafeSwitch is Tier-2 backlog — the block, not a crash, is the pass).

## Result

**❌ FAIL — both branch verbs failed intent parsing; the dirty-switch guard was never reached.**

**Expected:** (a) `feature-x` created + switched onto; (b) with a dirty tree, `checkout main` **blocked with a clear message** (no crash, no data loss).

**Actual — two separate parse failures:**

1. **Create-branch not recognized.** `gitrust "create branch feature-x"` (@ llm ~16.5s) printed a branch **listing** and `Nothing to do.` — it never created the branch:
   ```
   * main
     origin/main
     Nothing to do.
   ```
   Confirmed post-state: `git branch -a` shows only `main` + `origin/main`; **no `feature-x`**. The create intent fell through to a branch-list.

2. **Checkout couldn't extract the target.** `gitrust "checkout main"` (@ llm ~10.1s) returned:
   ```
   ✗  No target branch specified. Try: gitrust "checkout <branch-name>"
   ```
   The branch name `main` was literally in the phrase but not extracted — so the command aborted before ever hitting the dirty-switch check.

**Consequence:** the assertion under test (dirty switch is blocked, not crashed) was **not evaluable** — both setup steps failed. No crash and no data loss (`app.txt` edit preserved as `M app.txt`, still on `main`), but the feature could not be exercised.

**Additional observation — wrong path marker:** both commands showed `@ (llm · …)`. A plain `checkout <branch>` should be a **fast-path (`*`)** deterministic command, not an LLM round-trip. It went through the model *and still* failed to parse the target — a double miss (unnecessary latency + parse failure).

**Likely root cause:** intent extraction for the branch verbs (`create branch <name>`, `checkout <name>`) is not pulling the trailing argument out of the phrase — either the phrase→intent table lacks these forms or the argument slot isn't captured. Same family as M-04 (arguments/qualifiers dropped during routing).

**Repro:** deterministic (parse-layer failure, not model variance).

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
