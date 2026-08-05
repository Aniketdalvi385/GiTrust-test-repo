# M-10 · Sync with main via origin/HEAD

| | |
|---|---|
| **LLM** | yes |
| **Flagship** | — |
| **Result** | ❌ FAIL |
| **Run date** | 2026-08-04 |

## What this proves

Default branch resolved via origin/HEAD.

## Procedure

**Setup:**
```bash
mk_sandbox m10
git remote set-head origin --auto
git checkout -b feature
mk_teammate m10        # advances the default branch
git fetch -q
```

**Steps:**
```bash
$GITRUST "sync with main"   # ChoiceGate → REBASE
```

**Expect:** target resolves to the default branch automatically; rebase/merge offered; after Rebase on this *unpublished* branch: no force-push drama (no upstream); feature now contains main's commit.

## Result

**❌ FAIL — the sync intent was lost entirely; the tool rendered a plain status instead.**

**Setup was correct** (not the cause): `git remote set-head origin --auto` → `origin/HEAD set to main`; teammate advanced the default branch; sanity log showed the split clearly:
```
1fb2d6a (origin/main, origin/HEAD) teammate: hotfix
baeb2f0 (HEAD -> feature, main) base
```

**Expected:** `"sync with main"` resolves the target via `origin/HEAD` → offers a rebase ChoiceGate → rebases `feature` onto `1fb2d6a` so `feature` contains `teammate: hotfix` (unpublished branch → no force-push drama).

**Actual:** `gitrust "sync with main"` (**@ llm · ~19.6s** — model *was* consulted) ignored the sync intent and printed a **read-only status**:
```
On branch feature · no upstream
Last commit: baeb2f0 "base" (1m ago)
Nothing to commit, working tree clean.
→ No upstream set. Try: gitrust "publish"
```
No `origin/HEAD` resolution, no ChoiceGate, no rebase. After-state confirms nothing happened: `git log` shows `feature` still at `baeb2f0 base`; **`teammate: hotfix` is absent from `feature`** (verified by grep). `git status -sb` → `## feature`.

**Severity — worst instance of the argument/intent-drop pattern so far:** unlike M-04/M-05 (phrase-table gaps that at least routed *somewhere* branch-related), here the **LLM classifier itself** misread a target-carrying sync/rebase request as a read-only status. The entire intent was dropped, not just an argument. It also latched onto the "no upstream" surface fact and suggested `publish` — plausible-looking but wrong for the request.

**Note:** the "no upstream" reply is a red herring — `sync with main` is about the *local* relationship to the default branch, which needs no upstream on `feature`. The tool conflated "branch has no upstream" with "nothing to sync."

**Repro:** LLM-path — may vary run-to-run, but the failure mode (target-carrying request classified as status) is consistent with M-04/M-05/M-08's argument-loss family. Worth a re-run to check determinism, but the capability is clearly not reliably wired.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
