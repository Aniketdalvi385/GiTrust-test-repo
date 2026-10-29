# GiTrust v0.5.0 — acceptance report

**Date:** 2026-10-16 · **Binary:** `gitrust 0.5.0` (Glit `v0.5.0-fixes` at `887670b`) · **Model:**
`AniketDalvi385/gitrust-kev-0.8b@v2` (T = 4.0, MLX, Apple M2 8 GB)
**Suite:** 48 tests (M-00…M-42 with v0.5 expectations, M-43…M-47 new — one per 🔴 finding)
**Eval:** the same 450 requests as v0.4.1, through the binary.
**Fix plan and record:** in the GiTrust repo,
[`docs/v0.5.0_fix_plan.md`](https://github.com/Aniketdalvi385/gitrust/blob/v0.5.0-fixes/docs/v0.5.0_fix_plan.md)
— root causes, decisions D1–D9, F21–F31 found during the work.

## How this run was done

1. **Automatic run** — `suite/run.py auto` (4 shards): a pseudo-terminal drove the release binary
   for every test, pressing the keys each test lists, and checked the exit code, the repository
   and the screen. Each test ran in its own scratch `HOME`, bare remote and clone.
2. **Screen review** — three review agents read every recorded screen against the v0.5.0
   conventions and wrote `results/<id>/review.md`, with a line on what changed since v0.4.1. Their
   claims that mattered were re-checked against the screens and the source before going in here.
3. **Fixes from the review** — the review found four more (F28–F31, below). They were fixed in
   Glit `887670b`, each with a unit test seen failing without its fix; the suite gained checks
   for them (`4a57ce4`) and the seven affected tests (M-08, M-10, M-13, M-14, M-43, M-45, M-46)
   were re-run on the rebuilt binary, M-44 once more on its own (timing). Their reviews say what
   changed.
4. **Eval** — `eval/run_eval.py`: each request ran as `gitrust --yes "<request>"` in a fresh dirty
   repo (or one stopped mid-rebase / mid-merge / mid-cherry-pick, or — new — on a pushed feature
   branch that main has moved past, for the twelve requests that bring main into "my branch").
   The review fixes don't touch routing or anything `--yes` reaches, so the eval wasn't re-run.
5. **Flagship tests by hand** — the four ★ tests (M-04, M-06, M-16, M-23) were re-run by the
   owner in `manual` mode, driving every prompt (2026-10-16 and 2026-10-29). All four pass their
   automatic checks; records in `results/<id>-manual/`, matching the automatic runs. Two first
   attempts failed for reasons outside GiTrust and were re-run: M-06, a suite bug (manual runs
   recorded no per-step screens, fixed in `b8a1733`), and M-16, where the keep-staged option was
   picked instead of throw-away.
   Suite commits: 40 tests ran at `f5f0b76`, the eight re-runs at `4a57ce4`, the hand runs at
   `b8a1733` (`environment.json` names the last); the later commits only add checks or fix the
   harness.

## Result

| | v0.4.1 | **v0.5.0** |
|---|---|---|
| Automatic checks | 40 / 43 | **48 / 48** |
| After screen review | 19 ✅ · 21 ⚠️ · 3 ❌ | **20 ✅ · 28 ⚠️ · 0 ❌** |
| ★ Flagships by hand (owner) | M-04 ✅ · M-06 ⚠️ · M-16 ⚠️ · M-23 ✅ | **M-04 ⚠️ · M-06 ⚠️ · M-16 ⚠️ · M-23 ✅ — all automatic checks pass; the notes are copy** |
| Raw error chains (`caused by:`) on any screen | M-05, M-27, eval | **none** |
| Behaviour wrong or unsafe | none in the suite (F19, F21 found later) | **none** |

The ⚠️ count is not a step back: the conventions are stricter (one confirmation, no git output on
step lines, no Cancel rows), five tests are new, and the reviewers were told to note polish. Every
⚠️ is copy or layout — the notes are collected under [What's left](#whats-left).

| Eval set | n | right | asked (menu) | wrong, read-only | **wrong, changes something** | argument asked |
|---|---|---|---|---|---|---|
| v1 — 44-case paper set | 44 | 39 (89%) — was 39 | 4 — was 5 | 0 | **0** — was 0 | 1 — was 1 |
| v2 — owner's 68 phrasings | 68 | 56 (82%) — was 56 | 12 | 0 | **0** — was 0 | 0 |
| v3 — blind, 3 personas | 338 | 282 (83%) — was 282 | 54 — was 51 | 1 | **1** — was 3 (4 by the run-time rule) | **2** — was 9 |

Against the plan's acceptance: v1 and v2 hold with no wrong actions ✅; arg-asked ≤ 3 ✅; v3 "0
wrong actions that change something" is missed by one row, which changes nothing:

- **V3-024** "save all my work with message 'add login page'" → Kev picks *Push only some changes*
  (0.69); GiTrust finds no topic in the words and stops: "Couldn't find the feature/topic to push
  in your request — nothing was done.", exit 1. Interactively it would ask which topic. v0.4.1 does
  exactly the same; its row lost the "changes something" label only because v0.4.1 was re-scored
  from saved output, which skips that label. A model miss with no side effect — left as is.

Row by row against v0.4.1 (everything else is identical):

| Request | v0.4.1 | v0.5.0 |
|---|---|---|
| "Pull the latest from origin into this branch." | ⚡ *Update from main* (F3) | ✦ *Pull* ✅ |
| "Update my branch from upstream; CI is red…" | ⚡ *Update from main* (F3) | asks |
| "Park my local modifications on the stash stack." | *Restore stashed changes* at 0.91 (F4) | asks — the stash-direction check (D9) |
| "put my unfinished work aside, i will come back later" | *Stash* ✅ | asks — the same check, the safe way round |
| Six scoped-push / branch-name requests (F5) | routed, argument asked | routed, argument captured ✅ |
| "undo the last three commits" | menu | refused with the alternatives (squash / revert / undo one), exit 1 |

The fixture change: twelve requests ("update my branch with main", …) presuppose a feature branch;
in v0.4.1 they ran on `main`. They now run on a pushed feature branch that main has moved past,
and v0.4.1 was re-run on those twelve with the new fixture
([`../v0.4.1/eval/feature_rescore.json`](../v0.4.1/eval/feature_rescore.json)): 12/12, the same
as before, so v0.4.1's totals stand and the comparison is like for like.

## The v0.4.1 findings, closed

| # | | Finding | Now | Evidence |
|---|---|---|---|---|
| F1 | 🔴 | Panic on a closed pipe | exit 0, nothing on stderr | M-41 |
| F2 | 🟠 | Raw error chain when the trash can't be written | "Couldn't back up your files first, so nothing was deleted. Check that ~/.gitrust/trash is writable.", exit 1 | M-27 |
| F3 | 🔴 | "pull … into this branch" ran a sync with main | a pull of this branch | M-44, eval |
| F4 | 🟠 | stash ↔ stash pop | deterministic direction check; empty stash said plainly | M-47, eval |
| F5 | 🟠 | Argument capture gaps | topics, comma'd branch names, "with message '…'" kept | M-04, eval (9 → 2) |
| F6 | 🟠 | Side effects before the plan | the rescue's branch is the plan's first step; `q` leaves nothing | M-13, M-14, M-46 |
| F7 | 🔴 | Paused-pipeline snapshot trap | handed-off snapshots are never restored; no banner | M-08, M-45 |
| F8 | 🟠 | Hook failure dead-end | hook output once, then one message naming the staged files and the next step | M-21 |
| F9 | 🟠 | Double confirmation | one: the plan asks for the typed word in place of Enter | M-16, M-20, M-22 |
| F10 | 🟠 | Old menus with Cancel rows | numbered, no Cancel row anywhere (a source test forbids them) | M-13, M-14 |
| F11 | 🟠 | Deleting untracked files on Enter | the plan asks for `delete` | M-26 |
| F12 | 🟡 | Raw git output on step lines | hidden on success, shown once on failure | M-06, M-08, M-10, M-20, M-22, M-26 |
| F13 | 🟡 | Redundant "Consider pulling first" | gone | M-06, M-07 |
| F14 | 🟡 | Squash pre-filled the message | empty prompt, old subjects listed above it | M-19 |
| F15 | 🟡 | `--yes` refusal with the model down | its own sentence; no menu prompt pasted in | M-29 |
| F16 | 🟡 | Exit codes for empty results | D4: queries 0 (M-25), "nothing to recover" 1 (M-28) | M-25, M-28 |
| F17 | 🟡 | Copy: risks, echo, stash browser, pause, no-terminal advice | fixed | M-16, M-18, M-24, M-08, M-38 |
| F18 | 🟠 | Raw libgit2 error on a dirty switch | refused before the plan, naming the file | M-05 |
| F19 | 🔴 | "merge X into Y" ignored X / ran backwards | brings in the branch named; a destination that isn't this branch is refused | M-43 |
| F20 | 🟠 | A recovery drafted the commit message "update" | the recovery asks for the message (D8) | unit tests |

F21–F27 were found while fixing these — two of them lost uncommitted work in v0.4.1 (a
fast-forward's forced checkout; hard-reset backups that skipped staged changes). Details and
fixes are in the plan; each has unit tests.

## Found by this run, fixed before release

| # | | Finding | Fix | Evidence |
|---|---|---|---|---|
| F28 | 🟠 | "merge develop into feature" opened the rebase-vs-merge menu on **Rebase** — the request's word was parsed, then dropped | the strategy the request names is listed first | M-43 (re-run) |
| F29 | 🟠 | Merging another branch into a **never-pushed** branch published it (the rebase path deliberately doesn't) | no push; "publish it with gitrust "publish"" | M-43 (re-run) |
| F30 | 🟠 | A conflict pause didn't say the plan's **push never ran**; after `continue rebase` the footer said `Next: gitrust "status"` at ↑1 | the pause says so; the footer names the push | M-08, M-45 (re-run) |
| F31 | 🟡 | The detached-HEAD rescue for a **switch** said "your request runs on" the new branch, which the switch leaves | "keeps this commit; then you switch to main" | M-14 (re-run) |

## What's left

Polish the reviewers noted, none of it wrong behaviour — backlog for the next release:

- **A network step is drawn twice** — `○  push …` stays above `✓  push …` (M-04, M-06, M-07, M-20,
  M-37, M-44). Deliberate: the running line is ended before git may ask for credentials, so a
  prompt never lands mid-line. The most visible rough edge.
- **Long one-line messages don't wrap** (the plan's explanation blocks do) — M-16, M-18, M-21.
- **Menus:** the help line says "1–9" whatever the row count (M-34, M-43); hints are cut with "…"
  at a fixed 100 columns, not the terminal's width (M-15, M-16, M-31).
- **Internal words in copy:** "trash-net", "fail-closed", "retention window" (M-26, M-27);
  "pipeline" (M-28, M-45); "This op" (M-16); "⛔ Irreversible" above a line saying how to recover
  (M-20, M-26, M-27); "1 commit(s)".
- **"find my lost work" doesn't look in `~/.gitrust/trash`**, and its empty result doesn't mention
  that GiTrust's own discards are backed up there (M-25) — a small gap in what it does.
- Smaller: a deliberate pause is drawn with two ✗ (M-08, M-45); aborting reports a backup the
  plan didn't mention (M-09); a closing note prints after "Next:" (M-10, M-43); "clean up my repo"
  is echoed as *Discard uncommitted changes* when only untracked files would go (M-27); the
  piped "*" fallback for ⚡ sits next to Unicode ✗ (M-17, M-30).
- Timing: M-44's model call took 32 s in the sharded run and 9 s alone in the suite, but
  0.5–1.3 s in isolation — the first call after the release builds had pushed the model out of
  memory on the 8 GB machine, not GiTrust.

## What held up

- **Every v0.4.1 failure is gone** — the closed pipe, the trash-unwritable chain, the raw
  libgit2 error — and no screen in the run shows a `caused by:` chain.
- **One confirmation, after the plan, everywhere:** destructive plans take the typed word or
  branch name in place of Enter (M-16, M-20, M-26, M-27); back-outs stay calm and exit 1 (M-31,
  M-32, M-46).
- **Recovery and the trash-net:** a deleted branch and a dropped stash come back on `rescue/*`
  (M-23, M-24, the internal "index on …" row gone); a pause never leaves a snapshot that
  `--recover` would restore over finished work (M-45).
- **Routing:** the request's words decide source and direction (M-43, M-44); the model never acted
  wrongly in the suite; across the 112 owner/paper eval requests, never on something that changes
  the repository.

## Compared with v0.4.1

v0.4.1 ended 19 ✅ · 21 ⚠️ · 3 ❌ on 43 tests and left 20 findings, three of them 🔴 wrong actions or
traps (F3, F7, F19) plus one crash (F1). v0.5.0 closes all 20, plus eleven found along the way (two
that lost uncommitted work in v0.4.1), passes all 48 automatic checks and ends with no ❌. On the
eval it keeps every right answer and removes three of v0.4.1's four writes on the wrong
operation; the remaining one stops before doing anything.
