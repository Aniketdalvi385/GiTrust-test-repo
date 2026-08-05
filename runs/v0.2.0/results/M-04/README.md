# M-04 · Scoped feature pipeline ★

| | |
|---|---|
| **LLM** | yes |
| **Flagship** | ★ |
| **Result** | ❌ FAIL |
| **Run date** | 2026-07-31 |

## What this proves

Resolver related/unrelated grouping.

## Procedure

**Setup:**
```bash
mk_sandbox m04
echo "login page" > login.txt; echo "login helper" > auth.txt; echo "unrelated" > readme.txt
```

**Steps:**
```bash
$GITRUST "push the login changes"
git show --stat origin/$BR
```

**Expect:** resolver classifies `login.txt`/`auth.txt` related, `readme.txt` unrelated/uncertain; multi-select gate reflects that; after confirm, **only selected files** committed + pushed.

## Result

**❌ FAIL — flagship scoped-grouping capability did not engage.**

**Expected:** resolver classifies `login.txt` + `auth.txt` as login-related and `readme.txt` as unrelated → multi-select gate reflecting that grouping → after confirm, **only `login.txt` + `auth.txt`** committed & pushed; `readme.txt` left untracked.

**Actual:** `gitrust "push the login changes"` (@ llm ~27.2s) was routed as a **bare `push` intent**, not a scoped commit:
1. Prompted `Push 'main' to origin?` → then `Nothing committed yet — push alone won't ship your local edits.`
2. Offered a generic recovery: `Stage all → commit → push`.
3. Executed a 3-step plan: **`stage all modified files`** → commit `"update"` → push.

No resolver grouping, **no multi-select gate**, and the scope phrase ("the login changes") was dropped entirely. The generic subject `"update"` confirms the model was never asked to scope or describe the change.

**Damage confirmed** — the pushed commit contains **all three files**:
```
3782e5b "update"
 auth.txt   | 1 +
 login.txt  | 1 +
 readme.txt | 1 +   ← should NOT be here
 3 files changed, 3 insertions(+)
```
`readme.txt` (the unrelated file) was staged, committed, and pushed along with the login files. The core assertion — *only selected files committed + pushed* — is violated.

**Likely root cause:** intent routing treats `"push the login changes"` as intent=push and discards the scope qualifier, so it never enters the file-relatedness resolver / multi-select path. The scoped-commit pipeline is either not wired to this phrasing or is gated behind a different verb.

**Repro:** deterministic — the routing is not model-variance; it's a phrase→intent mapping miss.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).
Recording: see [`recording.md`](recording.md).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
