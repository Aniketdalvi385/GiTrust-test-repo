# GiTrust v0.5.0 — acceptance run

- **Binary:** `gitrust 0.5.0`
- **Model:** `AniketDalvi385/gitrust-kev-0.8b@v2` (T=4.0)
- **How:** `suite/run.py auto` — a pseudo-terminal drives the release binary, presses the keys each test lists, then checks exit code, repository and screen; every result was then reviewed from its screens (`review.md`). ★ = flagship, also run by hand (`suite/run.py manual`).
- **Report:** [REPORT.md](REPORT.md)

**Result:** 21 ✅ PASS · 31 ⚠️ PASS-WITH-NOTES

| ID | Test | Since | Mode | Result | Note |
|---|---|---|---|---|---|
| [M-00](results/M-00/) | Binary version and help | v0.2 | auto | ✅ PASS | gitrust 0.5.0; help is a clear, accurate cheat-sheet (unchanged from v0.4.1). |
| [M-01](results/M-01/) | Exact phrase works with the model down | v0.2 | auto | ✅ PASS | "status" works instantly with the model down: ⚡ line, no model complaint, remote age stated. |
| [M-02](results/M-02/) | Model classification of a read-only request | v0.2 | auto | ✅ PASS | Model asked a which-did-you-mean menu; the picked history ran with a ◇ line, exit 0. |
| [M-03](results/M-03/) | Commit: the message is yours, [e] edits it | v0.2 | auto | ✅ PASS | The message is the user's, the plan shows it, [e] re-opens it with the typed text; committed, exit 0. |
| [M-04](results/M-04/) | Scoped push: only the login files ★ | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Topic survives the quoted message: login files pre-selected, 'login page' offered, only they pushed; push line drawn twice. |
| [M-04-manual](results/M-04-manual/) | Scoped push: only the login files ★ | v0.2 | manual | ⚠️ PASS-WITH-NOTES | By hand: the topic survived the quoted message — login files pre-selected, 'login page' offered and kept, only they pushed; the push line is drawn twice, as in the automatic run. |
| [M-05](results/M-05/) | Create a branch; dirty switch is handled | v0.2 | auto | ✅ PASS | Branch created; the dirty switch is refused before any plan in one plain sentence naming app.txt; "Already on main." exits 0. |
| [M-06](results/M-06/) | Diverged push → rebase → pushed ★ | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Diverged push: plain rebase/merge choice, rebase + push in one plan, no warning or git noise; push line drawn twice. |
| [M-06-manual](results/M-06-manual/) | Diverged push → rebase → pushed ★ | v0.2 | manual | ⚠️ PASS-WITH-NOTES | By hand: diverged push → plain rebase/merge choice with both hints whole, rebase + push in one plan, no warning, no git output; the push line is drawn twice. |
| [M-07](results/M-07/) | Diverged push → merge | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Merge path makes a two-parent merge commit and pushes; warning and cut hints gone; push line drawn twice. |
| [M-08](results/M-08/) | Rebase conflict → calm pause → continue | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Conflict pause names app.txt and says the push didn't run, no git noise, exit 1; continue is clean with no banner and points at the push. |
| [M-09](results/M-09/) | Abort rebase restores exactly | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Abort returns exactly to the pre-rebase commit, status clean; the result reports a backup the plan never mentioned. |
| [M-10](results/M-10/) | Sync feature with main | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Sync rebases feature onto origin/main with no push or force; the closing note is now clear but still sits after "Next:". |
| [M-11](results/M-11/) | Mid-rebase commit request names the rebase | v0.2 | auto | ✅ PASS | Commit request mid-rebase refused in one plain line naming continue/abort; exit 1, instant. |
| [M-12](results/M-12/) | Commit a resolved merge: two parents | v0.2 | auto | ✅ PASS | git's MERGE_MSG offered, shown in the plan, merge commit has two parents; model answers in 1.6s. |
| [M-13](results/M-13/) | Commit on a detached HEAD → rescue to a branch | v0.2 | auto | ✅ PASS | Detached-HEAD commit: numbered rescue menu without Cancel, the branch is the plan's first step, work committed on it. |
| [M-14](results/M-14/) | Switching away would strand a commit → guard | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Guard saves the stranded commit on a branch inside the plan, then switches to main; the copy now says the branch keeps the commit and the switch then leaves it. |
| [M-15](results/M-15/) | Undo: four plain options, keep staged | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Undo names the commit, four numbered options with consequences, keeps changes staged; two hints still cut with "…". |
| [M-16](results/M-16/) | Undo → throw away: type to confirm, trash backup ★ | v0.2 | auto | ⚠️ PASS-WITH-NOTES | One confirmation now (the SHA typed at the plan), honest Risks text, the result names the backup; menu hints cut and one warning wraps raggedly. |
| [M-16-manual](results/M-16-manual/) | Undo → throw away: type to confirm, trash backup ★ | v0.2 | manual | ⚠️ PASS-WITH-NOTES | By hand: one confirmation — the plan and its explanation, then '0059c01' typed in place of Enter; honest Risks; the result names the backup. Copy nits: "This op", and Recovery undersells "find my lost work". |
| [M-17](results/M-17/) | --yes cannot undo | v0.2 | auto | ⚠️ PASS-WITH-NOTES | --yes refuses to choose an undo mode, lists the four choices, exit 1, HEAD untouched; the piped first line still uses "*" for ⚡. |
| [M-18](results/M-18/) | Undo 3 commits halts with guidance | v0.2 | auto | ⚠️ PASS-WITH-NOTES | The guard comes first now: no "Undo the last commit" echo, guidance, exit 1, nothing changed; the guidance wraps raggedly and revert has no phrase. |
| [M-19](results/M-19/) | Squash last 3: same content, one commit | v0.2 | auto | ✅ PASS | Squash asks for the message on an empty prompt with the three subjects listed above it; one Enter at a one-line plan; tree identical, exit 0. |
| [M-20](results/M-20/) | Fix a pushed commit's message: escalate + lease | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Plan first, then 'main' typed in place of Enter; force-with-lease, no git output, exit 0; the push step's running line stays on screen and the risk copy repeats itself. |
| [M-21](results/M-21/) | A failing pre-commit hook blocks the commit | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Hook output shown once under the step, then one plain message naming the staged file and the next step; no menu, exit 1. The message is cut mid-word by the terminal. |
| [M-22](results/M-22/) | Revert succeeds despite the same hook | v0.2 | auto | ✅ PASS | Revert succeeds past the pre-commit hook, as git does; one Enter at a plan that names the commit's subject; clean step output, exit 0. |
| [M-23](results/M-23/) | Deleted branch → find my lost work ★ | v0.2 | auto | ✅ PASS | The lost commit is listed in plain words and restored to a rescue branch; current branch and files untouched; exit 0. |
| [M-23-manual](results/M-23-manual/) | Deleted branch → find my lost work ★ | v0.2 | manual | ✅ PASS | By hand: the lost commit is listed in plain words and restored to a rescue branch; current branch and files untouched; exit 0. |
| [M-24](results/M-24/) | A dropped stash surfaces | v0.2 | auto | ✅ PASS | The dropped stash is listed on its own, without git's internal "index on …" row, and restored to a rescue branch holding the wip change; exit 0. |
| [M-25](results/M-25/) | Nothing lost: an honest empty result | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Honest "Nothing found", exit 0 as a query that ran (D4); still no next step, and no word about the trash backups of uncommitted work. |
| [M-26](results/M-26/) | Clean up: counts, untracked deleted, backed up | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Counts per kind, 'delete' typed at the plan, only the untracked file deleted and backed up, result says "deleted files"; the explanation block is full of internal words. |
| [M-27](results/M-27/) | Backup can't be written → nothing deleted | v0.2 | auto | ⚠️ PASS-WITH-NOTES | After the typed word, one plain refusal under the step (couldn't back up, nothing deleted, check ~/.gitrust/trash); file kept, exit 1. The plan shares M-26's internal words. |
| [M-28](results/M-28/) | --recover with nothing to recover points to forensics | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Nothing interrupted, points to "find my lost work", now exits 1 (D4); "pipeline" is an internal word. |
| [M-29](results/M-29/) | Model down: warning, full menu, refusals | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Model down: warning with the fix, full titled menu, its own --yes refusal (F15), no-terminal advice without --yes (F17), instant status; run 2 says the problem and fix twice. |
| [M-30](results/M-30/) | Not a repository | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Plain not-a-repository message with the fix, exit 1; the piped first line still uses "*" for ⚡. |
| [M-31](results/M-31/) | Esc at a menu: calm cancel, exit 1, nothing done | v0.4 | auto | ⚠️ PASS-WITH-NOTES | Esc at the undo menu: one calm "↪ Canceled — nothing was done.", exit 1, HEAD untouched; the only note is two menu hints cut with "…". |
| [M-32](results/M-32/) | q at the plan cancels; stray keys are ignored | v0.4 | auto | ✅ PASS | The stray key did nothing, q cancelled with "Canceled — nothing was done.", exit 1, nothing committed. |
| [M-33](results/M-33/) | [s] at the plan: commit stays local | v0.4 | auto | ✅ PASS | [s] drops the push step and redraws a 2-step plan; the commit stays local (↑1), exit 0. |
| [M-34](results/M-34/) | Numbered menu: a digit chooses at once | v0.4 | auto | ⚠️ PASS-WITH-NOTES | 9 was ignored and 2 chose "keep the changes in my files" at once; the commit was undone with its changes unstaged, exit 0. The menu hint offers digits the menu doesn't have. |
| [M-35](results/M-35/) | Learned phrase: a menu pick is instant next time | v0.4 | auto | ⚠️ PASS-WITH-NOTES | The menu pick was learned, ran instantly with the model down ("⚡  Show status · learned"), was listed by `aliases` and forgotten cleanly; one ordering nit remains. |
| [M-36](results/M-36/) | Not a Git request: refused, exit 1 | v0.4 | auto | ✅ PASS | A polite refusal in 1.6s pointing at examples and `gitrust help`, exit 1. |
| [M-37](results/M-37/) | Commit and push in one request | v0.4 | auto | ⚠️ PASS-WITH-NOTES | "commit n push" was routed by the model, asked for the message, then committed and pushed, exit 0. A new leftover "○ push" line and a "commit(s)" plural are polish. |
| [M-38](results/M-38/) | No terminal, a question needed: plain message, exit 1 | v0.4 | auto | ✅ PASS | One plain line, exit 1, and the advice now says --yes won't choose instead of suggesting it. |
| [M-39](results/M-39/) | Status mid-rebase says what to do | v0.4 | auto | ⚠️ PASS-WITH-NOTES | Mid-rebase status names the rebase, the conflicted file and the continue/abort phrases (exit 0), but its header never names the user's branch. |
| [M-40](results/M-40/) | Clean tree: 'commit everything' stops before asking | v0.4 | auto | ✅ PASS | The clean tree is caught before any message prompt with a plain "Nothing to commit", exit 1. |
| [M-41](results/M-41/) | Output piped into head doesn't crash | v0.4 | auto | ✅ PASS | No panic when the pipe's reader is already gone; the run completes with exit 0 (D5). |
| [M-42](results/M-42/) | Help lists only phrases that work instantly | v0.4 | auto | ✅ PASS | Every phrase in help's Look section works instantly with the model down; the help text matches the v0.5.0 conventions. |
| [M-43](results/M-43/) | 'merge develop into feature' brings in develop, not main | v0.5 | auto | ⚠️ PASS-WITH-NOTES | F19 is fixed: "⚡ Update from develop" merges origin/develop, not main; the menu opens on Merge (the request's word) and the never-pushed feature isn't published. |
| [M-44](results/M-44/) | 'Pull the latest from origin into this branch' is a pull | v0.5 | auto | ⚠️ PASS-WITH-NOTES | F3 is fixed: "pull the latest from origin into this branch" became "✦ Pull from origin", feature got origin/feature's commit and not main's, exit 0. The routing took 31.9s, and the plan line is vague. |
| [M-45](results/M-45/) | Rebase finished with plain git: no stale banner, --recover undoes nothing | v0.5 | auto | ⚠️ PASS-WITH-NOTES | F7 is fixed: after the rebase was finished with plain git, status shows no banner and `--recover` restores nothing (exit 1, HEAD kept). The pause now says the push didn't run; the two ✗ marks and "pipeline" remain. |
| [M-46](results/M-46/) | Detached-HEAD rescue: q at the plan changes nothing | v0.5 | auto | ⚠️ PASS-WITH-NOTES | F6 and F10 are fixed: the rescue is a numbered menu with no Cancel row, the new branch is the plan's first step, and q at the plan leaves nothing behind ("Canceled — nothing was done." is now true), exit 1. Only copy nits remain. |
| [M-47](results/M-47/) | Bring back a stash when there is none: plain message, exit 1 | v0.5 | auto | ✅ PASS | F4 is fixed: "stash pop" with no stash is blocked before any plan with "There are no stashed changes to bring back.", exit 1, and the edit is untouched. |

## Eval (whole system, `gitrust --yes`, dirty repo)

Model `AniketDalvi385/gitrust-kev-0.8b@v2`. Details: [eval/](eval/).

| Set | n | right | asked (menu) | wrong, read-only | wrong, changes something |
|---|---|---|---|---|---|
| v1_44 | 44 | 39 (89%) | 4 | 0 | 0 |
| v2_owner_68 | 68 | 56 (82%) | 12 | 0 | 0 |
| v3_blind | 338 | 282 (83%) | 54 | 1 | 1 |
