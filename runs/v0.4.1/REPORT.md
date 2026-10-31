# GiTrust v0.4.1 — acceptance report

**Date:** 2026-10-15 · **Binary:** `gitrust 0.4.1` (Glit `9009a73`+docs) · **Model:**
`AniketDalvi385/gitrust-kev-0.8b@v2` (T = 4.0, MLX, Apple M2 8 GB)
**Suite:** 43 tests (M-00…M-30 carried over from v0.2/v0.3 with v0.4 expectations, M-31…M-42 new)
**Eval:** 450 requests in three held-out sets, through the binary.
**Fix plan:** in the GiTrust repo,
[`docs/v0.5.0_fix_plan.md`](https://github.com/Aniketdalvi385/gitrust/blob/main/docs/v0.5.0_fix_plan.md) —
all 20 findings, root causes in source, batches, decisions.

## How this run was done

1. **Automatic run** — `suite/run.py auto`: a pseudo-terminal drove the release binary for every
   test, pressing the keys each test lists, and checked the exit code, the repository and the
   screen. Each test ran in its own scratch `HOME`, bare remote and clone.
2. **Screen review** — three review agents read every recorded screen against the product's
   conventions and wrote `results/<id>/review.md` (verdict + notes). Their claims that
   mattered were re-checked against the screens before going into this report.
3. **Eval** — `eval/run_eval.py`: each request ran as `gitrust --yes "<request>"` in a fresh
   dirty repo (or a repo stopped mid-rebase / mid-merge / mid-cherry-pick).
4. **Flagship tests by hand** — the four ★ tests (M-04, M-06, M-16, M-23) were re-run by the
   owner in `manual` mode, driving every prompt, and screen-recorded in [`evidence/`](evidence/).
   All four pass their automatic checks; their records are `results/<id>-manual/` and match the
   automatic runs.

## Result

| | |
|---|---|
| Automatic checks | **40 / 43 pass** — the 3 failures are real bugs (F1, F2, F18) |
| After screen review | 19 ✅ PASS · 21 ⚠️ PASS-WITH-NOTES · 3 ❌ FAIL |
| ★ Flagships by hand (owner, recorded) | M-04 ✅ · M-06 ⚠️ · M-16 ⚠️ · M-23 ✅ — all automatic checks pass |
| Behaviour wrong or unsafe | **none** — F2/F18 are safe but print raw errors; F1 is a crash on a closed pipe. No data lost, no wrong exit codes on back-outs, every destructive op gated |

| Eval set | n | right | asked (menu) | wrong, read-only | **wrong, changes something** |
|---|---|---|---|---|---|
| v1 — 44-case paper set | 44 | 39 (89%) | 5 | 0 | **0** |
| v2 — owner's 68 phrasings | 68 | 56 (82%) | 12 | 0 | **0** |
| v3 — blind, 3 personas (new) | 338 | 282 (83%) | 51 | 1 | **3** (F3, F4) |

"Right" includes 9 requests that routed correctly but whose argument (topic, branch name, count)
wasn't captured from the words — interactively GiTrust asks for it; under `--yes` it stops (F5).
v3 by persona: newcomer 83%, senior 82%, casual 85%. Of its 25 out-of-scope requests 9 were
refused and 16 got a menu (none acted). Most other menus were for discard/undo requests — the
higher bar for destructive operations doing its job.

**v3 is the first eval written blind to the training data** — three persona agents that saw
only plain-English operation descriptions, never the training phrasings or earlier sets; labels
checked by an independent annotator (338/338 agree); 31 near-duplicates of training phrasings
removed. It lands within a few points of the owner's own set — evidence the fine-tune
generalises beyond one person's phrasing. Caveat: the training templates were also written with
Claude, so v3 is independent of the training *data* but not of the model family that wrote it;
real users' phrasings remain the stronger test.

## Findings

Severity: 🔴 wrong action or crash · 🟠 misleading / inconsistent behaviour · 🟡 copy and polish.

| # | | Finding | Evidence |
|---|---|---|---|
| F1 | 🔴 | **Panic on a closed pipe.** `gitrust --yes "show history" \| head -1` → `failed printing to stdout: Broken pipe`, exit 101. Fix: ignore `BrokenPipe` on output (or reset SIGPIPE). | M-41 |
| F2 | 🟠 | **Raw error chain when the trash can't be written.** Safe (nothing deleted, exit 1) but prints `caused by: Permission denied (os error 13)` and a long temp path, twice, and never says "nothing was deleted". | M-27 |
| F3 | 🔴 | **Exact-phrase rule misroutes "pull … into this branch" to sync.** "Pull the latest from origin into this branch." and "Update my branch from upstream; …" → ⚡ *Update from main* (merge main), not *Pull*. Deterministic, so the model can't save it. | eval v3 |
| F4 | 🟠 | **One confident model miss: stash ↔ stash pop.** "Park my local modifications on the stash stack." → *Restore stashed changes* at 0.91. Failed harmlessly (no stash) but with a raw `caused by: reference 'refs/stash' not found` chain. (The `Recovery: Some(NoLocalChange …)` line seen in the eval output only prints under `GITRUST_DEBUG=1`, which the eval sets.) | eval v3 |
| F5 | 🟠 | **Argument capture gaps.** Routed right, argument missed: topics in "only … the login related files", "the search part of my code", "the billing module changes", "Only the auth changes …"; branch names after a comma ("a fresh branch, release/2.4") or in "Check out release/2.3"; "my last few commits" (no count). And "push the login changes **with message 'login page'**" loses the topic entirely. | eval v3, M-04 |
| F6 | 🟠 | **Side effects before the plan is confirmed.** The detached-HEAD rescue creates the branch and stages the changes *before* showing the plan; pressing `q` at the plan leaves them. | M-13, M-14 |
| F7 | 🔴 | **The paused-pipeline snapshot is a trap.** After a deliberate conflict pause, the next command shows "An interrupted pipeline was found — run `gitrust --recover`". `continue rebase` via GiTrust clears it afterwards, but if the rebase is finished with plain `git rebase --continue` the snapshot stays, and `--recover` on the now-clean repo would reset the branch to before the rebase — undoing the user's resolution (recoverable only via the reflog). Confirmed by reading `recovery_plan` (planning, not run). | M-08 |
| F8 | 🟠 | **Hook failure dead-end.** After a pre-commit hook blocks the commit: a "Pick one: Show / Cancel" menu (a Cancel row), and Esc says "Canceled — nothing was done." although the files stay staged. | M-21 |
| F9 | 🟠 | **Double confirmation.** Revert asks its own `(Y/n)` *and* then the plan prompt; undo-discard and pushed-amend ask type-to-confirm *and* the plan prompt. | M-22, M-16, M-20 |
| F10 | 🟠 | **Older menus break the conventions:** the detached-HEAD rescue menu is un-numbered and has a "Cancel" row (also "Create a branch HERE"). | M-13, M-14 |
| F11 | 🟠 | **Deleting untracked files has no typed confirmation** — the ⛔ plan + Enter only; the trash backup is their only copy. | M-26 |
| F18 | 🟠 | **Switching branches with an edit in the way shows a raw libgit2 error:** `caused by: 1 conflict prevents checkout; class=Checkout (20); code=Conflict (-13)`, twice, with no next step (commit / stash first). Safe — the edit survives, exit ≠ 0. | M-05 |
| F19 | 🔴 | **"merge/pull X into Y" ignores X and can run backwards** (found while planning, confirmed on the binary). The sync rule always uses origin's default branch: "merge develop into feature" and "pull develop into this branch" sync with *main*; "merge feature into main" (said on `feature`) brings main *into* feature — the opposite. The echo says "Update from main" and the gate names `origin/main`, and `--yes` refuses the gate, so it is never silent. | planning |
| F20 | 🟠 | **A recovery option drafts a commit message.** When a dirty tree blocks a pull, the "Commit → pull" recovery option commits everything with the hard-coded message `"update"` — breaking "GiTrust never writes your commit messages". (Found while planning, by reading the code.) | planning |
| F12 | 🟡 | **Raw git output leaks onto step lines** ("Successfully rebased…", "Enumerating objects…", "Removing junk/", `[main 4fe1afd] Revert …`, garbled "Auto-merging app.txtorigin/mainRebasing (1/1)"). | M-06, M-08, M-10, M-20, M-22, M-26 |
| F13 | 🟡 | **Redundant "Consider pulling first" warning** on a plan that already rebases/merges upstream. | M-06, M-07 |
| F14 | 🟡 | **Squash pre-fills the message with the three old subjects** joined — borderline against "never drafts a message"; the plan then shows a multi-line message. | M-19 |
| F15 | 🟡 | **`--yes` refusal with the model down** pastes the menu prompt mid-sentence ("… pick what you want to do (type to filter):") and lists all 35 operations. | M-29 |
| F16 | 🟡 | **Exit 0 when nothing was done:** "find my lost work" with nothing found, `--recover` with nothing to recover — decide whether these are queries (0) or not-done (1), and document it. | M-25, M-28 |
| F17 | 🟡 | The undo-discard "Risks" text says uncommitted work "is gone" and names only `git reflog`, while the same run backs it up to ~/.gitrust/trash (found by hand, M-16-manual). Smaller copy: "Undo the last commit" echoed for "undo the last 3 commits" before the halt; the dropped-stash browser lists the internal "index on main" commit; the conflict pause doesn't name the file; "already on main" not acknowledged; menu hints cut with "…"; the no-terminal advice suggests `--yes` for a case `--yes` refuses. | M-16, M-18, M-24, M-08, M-05, M-06, M-38 |

Not findings: the model sometimes asks a "which did you mean?" menu where it could have acted
(M-02 asked; M-35 relies on it) — that is the designed behaviour. A 14 s refusal in M-36 came
from four test shards sharing the model at once, not from the model itself.

## What held up

- **Every destructive path is gated and backed up:** undo-discard (typed confirm + trash backup),
  clean-up (backup of nested untracked files, M-26), fail-closed when the backup can't be written
  (M-27), pushed-history rewrite with `--force-with-lease` and a typed branch name (M-20).
- **Recovery works:** a deleted branch and a dropped stash both come back on `rescue/*` branches
  with HEAD untouched (M-23, M-24).
- **The v0.4 conventions hold everywhere they were tested:** Esc / `q` → "↪ Canceled — nothing
  was done." exit 1 (M-31, M-32, M-29); stray keys ignored; numbered menus; `[e]`/`[s]` plan
  keys; learned phrases work with the model down (M-35); not-Git requests refused with exit 1
  (M-36); no-terminal runs give one plain line (M-38); exact phrases work with the model down
  (M-01, M-42).
- **The model never acted wrongly in the suite**, and across 112 owner/paper eval requests not
  once on something that changes the repository.

## Compared with v0.3.0

v0.3.0 ended 40 ✅ · 2 ⚠️ · 0 ❌ on the original 31 tests (+ variants), with Ollama/qwen and the
embedding router, after three fix rounds. This run uses stricter conventions (exit codes on every
back-out, no Cancel rows, no raw errors) and 12 new tests, so the ⚠️ count is not comparable; the
three ❌ are all new checks (closed pipe, raw error chains). On the same 44 requests the qwen LLM
alone routed 41% (2026-08 research, exact phrases bypassed; corrected 2026-10-31: that run's prompt
was truncated to 2,048 tokens — with the whole prompt it routes 35/44, 80%); v0.4.1's whole system, exact
phrases included, gets 39/44 right and asks on the other 5.
