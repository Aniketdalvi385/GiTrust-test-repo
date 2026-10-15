# GiTrust v0.4.1 — acceptance run

- **Binary:** `gitrust 0.4.1`
- **Model:** `AniketDalvi385/gitrust-kev-0.8b@v2` (T=4.0)
- **How:** `suite/run.py auto` — a pseudo-terminal drives the release binary, presses the keys each test lists, then checks exit code, repository and screen; every result was then reviewed from its screens (`review.md`). ★ = flagship, also run by hand (`suite/run.py manual`).
- **Report:** [REPORT.md](REPORT.md)

**Result:** 3 ❌ FAIL · 19 ✅ PASS · 21 ⚠️ PASS-WITH-NOTES

| ID | Test | Since | Mode | Result | Note |
|---|---|---|---|---|---|
| [M-00](results/M-00/) | Binary version and help | v0.2 | auto | ✅ PASS | Version 0.4.1 and a clear, accurate help cheat-sheet. |
| [M-01](results/M-01/) | Exact phrase works with the model down | v0.2 | auto | ✅ PASS | Instant status with the model down, no model complaint. |
| [M-02](results/M-02/) | Model classification of a read-only request | v0.2 | auto | ✅ PASS | Model asked a which-did-you-mean menu; chosen history ran correctly. |
| [M-03](results/M-03/) | Commit: the message is yours, [e] edits it | v0.2 | auto | ✅ PASS | Message asked from user, shown in plan, [e] edit works, committed. |
| [M-04](results/M-04/) | Scoped push: only the login files ★ | v0.2 | auto | ✅ PASS | Picker pre-selects login files; only they were committed and pushed. |
| [M-05](results/M-05/) | Create a branch; dirty switch is handled | v0.2 | auto | ❌ FAIL | Branch created; dirty switch is safe but shows a raw libgit2 error chain. |
| [M-06](results/M-06/) | Diverged push → rebase → pushed ★ | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Diverged push rebased and pushed linearly; plan carries a contradictory warning. |
| [M-07](results/M-07/) | Diverged push → merge | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Merge path makes a merge commit and pushes; same warning/truncation nits. |
| [M-08](results/M-08/) | Rebase conflict → calm pause → continue | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Conflict pauses calmly with exit 1 and continue works; raw git noise and stale warning. |
| [M-09](results/M-09/) | Abort rebase restores exactly | v0.2 | auto | ✅ PASS | Abort rebase returns to the original HEAD; status shows no rebase. |
| [M-10](results/M-10/) | Sync feature with main | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Sync rebases onto main with no push; closing note is a bit confusing. |
| [M-11](results/M-11/) | Mid-rebase commit request names the rebase | v0.2 | auto | ✅ PASS | Commit mid-rebase refused clearly, naming the rebase options, exit 1. |
| [M-12](results/M-12/) | Commit a resolved merge: two parents | v0.2 | auto | ✅ PASS | Merge commit offered git's own message; two parents created. |
| [M-13](results/M-13/) | Commit on a detached HEAD → rescue to a branch | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Detached-HEAD commit rescued onto a branch; menu has Cancel row. |
| [M-14](results/M-14/) | Switching away would strand a commit → guard | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Guard warns stranded commit, saves branch first, then switches; menu nits. |
| [M-15](results/M-15/) | Undo: four plain options, keep staged | v0.2 | auto | ✅ PASS | Undo menu names the commit, four numbered options, keeps changes staged. |
| [M-16](results/M-16/) | Undo → throw away: type to confirm, trash backup ★ | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Typed confirm and trash backup work; double confirmation and truncated menu text. |
| [M-17](results/M-17/) | --yes cannot undo | v0.2 | auto | ✅ PASS | --yes refuses to pick an undo mode, lists choices, exits 1. |
| [M-18](results/M-18/) | Undo 3 commits halts with guidance | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Halts safely with guidance, but first line misstates the request as "last commit". |
| [M-19](results/M-19/) | Squash last 3: same content, one commit | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Squash works and tree is identical, but message prompt and plan rendering are messy. |
| [M-20](results/M-20/) | Fix a pushed commit's message: escalate + lease | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Reword of pushed commit escalates correctly with lease; raw git output leaks. |
| [M-21](results/M-21/) | A failing pre-commit hook blocks the commit | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Hook failure blocks commit and shows output, but Cancel row and misleading cancel text. |
| [M-22](results/M-22/) | Revert succeeds despite the same hook | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Revert works with exit 0, but uses its own Y/n question plus plan Enter. |
| [M-23](results/M-23/) | Deleted branch → find my lost work ★ | v0.2 | auto | ✅ PASS | Lists lost commit in plain words, restores to a rescue branch safely. |
| [M-24](results/M-24/) | A dropped stash surfaces | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Dropped stash is listed and restored; an internal index entry adds noise. |
| [M-25](results/M-25/) | Nothing lost: an honest empty result | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Clear "Nothing found" message, but exits 0 although nothing was done. |
| [M-26](results/M-26/) | Clean up: counts, untracked deleted, backed up | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Clean-up deletes only chosen untracked files with backup; wording and raw output nits. |
| [M-27](results/M-27/) | Backup can't be written → nothing deleted | v0.2 | auto | ❌ FAIL | Safe refusal (file kept, exit 1) but prints a raw "caused by:" error chain. |
| [M-28](results/M-28/) | --recover with nothing to recover points to forensics | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Says nothing interrupted and points to "find my lost work"; exits 0. |
| [M-29](results/M-29/) | Model down: warning, full menu, refusals | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Model-down warning and refusals are safe; --yes message is clunky and long. |
| [M-30](results/M-30/) | Not a repository | v0.2 | auto | ⚠️ PASS-WITH-NOTES | Friendly not-a-repo message with exit 1; piped first line uses "*" marker. |
| [M-31](results/M-31/) | Esc at a menu: calm cancel, exit 1, nothing done | v0.4 | auto | ✅ PASS | Esc at the undo menu cancels calmly, exit 1, HEAD untouched. |
| [M-32](results/M-32/) | q at the plan cancels; stray keys are ignored | v0.4 | auto | ✅ PASS | Stray key ignored, q cancels with exit 1, nothing committed. |
| [M-33](results/M-33/) | [s] at the plan: commit stays local | v0.4 | auto | ✅ PASS | [s] drops the push step; commit stays local, exit 0. |
| [M-34](results/M-34/) | Numbered menu: a digit chooses at once | v0.4 | auto | ✅ PASS | Invalid digit ignored; digit 2 picks instantly and unstages correctly. |
| [M-35](results/M-35/) | Learned phrase: a menu pick is instant next time | v0.4 | auto | ✅ PASS | Unclear phrase got a menu; pick learned, instant offline next time. |
| [M-36](results/M-36/) | Not a Git request: refused, exit 1 | v0.4 | auto | ⚠️ PASS-WITH-NOTES | Polite refusal with exit 1, but took 14.3s to decide. |
| [M-37](results/M-37/) | Commit and push in one request | v0.4 | auto | ✅ PASS | "commit n push" routed by the model; message asked, committed and pushed. |
| [M-38](results/M-38/) | No terminal, a question needed: plain message, exit 1 | v0.4 | auto | ⚠️ PASS-WITH-NOTES | One plain line, exit 1; piped first line shows "*" not ⚡. |
| [M-39](results/M-39/) | Status mid-rebase says what to do | v0.4 | auto | ✅ PASS | Mid-rebase status names rebase, conflicted file, and continue/abort phrases. |
| [M-40](results/M-40/) | Clean tree: 'commit everything' stops before asking | v0.4 | auto | ⚠️ PASS-WITH-NOTES | Clean tree stops before any prompt, exit 1; piped marker is "*". |
| [M-41](results/M-41/) | Output piped into head doesn't crash | v0.4 | auto | ❌ FAIL | Rust panic (exit 101) when piped output reader closes early. |
| [M-42](results/M-42/) | Help lists only phrases that work instantly | v0.4 | auto | ✅ PASS | Every Look-section phrase in help works instantly with the model down. |

## Eval (whole system, `gitrust --yes`, dirty repo)

Model `AniketDalvi385/gitrust-kev-0.8b@v2`. Details: [eval/](eval/).

| Set | n | right | asked (menu) | wrong, read-only | wrong, changes something |
|---|---|---|---|---|---|
| v1_44 | 44 | 39 (89%) | 5 | 0 | 0 |
| v2_owner_68 | 68 | 56 (82%) | 12 | 0 | 0 |
| v3_blind | 338 | 282 (83%) | 51 | 1 | 3 |
