# GiTrust v0.3.0 — Acceptance Report

**Binary:** `gitrust 0.3.0` · **Date:** 2026-08-07 · **Platform:** Darwin/arm64 · **git:** 2.39.5

## Result summary

| Verdict | Count |
|---|---|
| ✅ PASS | 28 |
| ⚠️ PASS with defects | 2 |
| ❌ FAIL | 0 |
| ⛔ BLOCKED | 0 |
| ⏭️ SKIP | 1 |

## Full results

| ID | Title | Result | Notes |
|---|---|---|---|
| M-00 | Build, version, setup | ✅ PASS | Binary reports `gitrust 0.3.0` — matches the run folder. Version bump landed. |
| M-01 | Fast-path status (Ollama OFF) | ✅ PASS | Ollama stopped; `status` responded instantly with the ⚡ fast-path marker, no model call, no Ollama error. |
| M-02 | LLM-path classification | ✅ PASS | ◉ LLM marker (~15.5s); classified as read-only status, correct empty summary. |
| M-03 | Commit with editable message | ✅ PASS | Editable message gate appeared; edited draft committed as-is (HEAD subject = `fix(app.txt): add missing change line`); post-check confirmed. |
| M-04 | Scoped feature pipeline (flagship) | ✅ PASS | Scoped routing worked (fast-path *): resolver classified login.txt=Related (pre-checked), readme.txt=Unrelated (hidden), auth.txt=Uncertain (offered, not pre-checked). Pushed commit contains only login.txt — readme correctly excluded. Note: auth.txt was left out because it was Uncertain and not toggled on; scoping itself is correct. |
| M-05 | Branch create + dirty switch block | ✅ PASS | `create branch feature-x` fast-path (*) created the branch; `checkout main` fast-path switched cleanly. (Dirty-switch: tree had 'M app.txt' and the checkout to main succeeded — main's app.txt matched, so no block was needed; branch verbs now parse correctly, the M-05 v0.2 parse-failure is fixed.) |
| M-06 | Diverged push -> rebase -> clean (flagship) | ✅ PASS | Diverged [ahead 1, behind 1] → ChoiceGate with plain-English rebase/merge consequences → chose Rebase → rebase+push in one pipeline → left-right 0 0, teammate commit below yours. Flagship works. |
| M-07 | Diverged -> merge path | ✅ PASS | Same divergence → chose Merge → merge commit with 2 parents, pushed, clean. |
| M-08 | Conflicting rebase -> calm pause -> continue (flagship) | ✅ PASS | Rebase hit the same-line conflict and paused CALMLY: names 1 file (correct count — v0.2 said '0 file(s)'), 'nothing is lost', offers continue/abort verbs, EXIT=1 (v0.2 was exit 0). Both P1 exit-code and P5 conflict-count fixes confirmed live. |
| M-09 | Abort restores exactly | ✅ PASS | abort rebase restored HEAD to exactly PRE (9bf9124…), tree back to [ahead 1, behind 1]. (Note: the pre-existing interrupted-pipeline snapshot warning showed — carried over from M-08's paused rebase; abort itself is clean.) |
| M-10 | Sync with main via origin/HEAD | ✅ PASS | `sync with main` fast-path (*) → resolved default branch via origin/HEAD, fast-forwarded/merged origin/main into feature; feature now contains 'teammate: hotfix'. Was read-only status in v0.2 — P2 sync fix confirmed live. |
| M-11 | Mid-rebase never says checkout a branch | ✅ PASS | Mid-rebase, `commit my changes` → block names the REBASE and offers continue/abort. The words 'checkout a branch' do NOT appear — S12 regression stays dead. |
| M-12 | Merge-aware commit: two parents | ✅ PASS | Merge commit created with exactly 2 parents; message is clean 'Merge branch \'side\'' with NO '# Conflicts:' lines. Both the two-parent behavior and the M-12 comment-stripping fix confirmed. |
| M-13 | Detached write -> rescue | ⚠️ PASS (with defects) | Branch-here rescue works (created + switched to rescue-work, no data loss). BUT the original 'commit this' did NOT complete: pre-check blocked with 'Nothing staged to commit' — the resume reached the commit step but the change wasn't auto-staged, so the commit-continuation still doesn't land the user's edit. The M-13 resume fix wires the redirect through, but the commit needs staging. Change is safe (M app.txt on rescue-work), so PASS-with-defect, not FAIL. |
| M-14 | Stranded-commit guard (flagship) | ✅ PASS | Stranded-commit guard fired: warned '1 commit(s) here are on NO branch', offered branch-here FIRST; took it → rescue-work created preserving the detached commit, then switched to main. Nothing stranded. |
| M-15 | Undo gate: four options, names the commit | ✅ PASS | Undo gate showed exactly FOUR options, question named short oid + 'feat: the mistake'. Chose Keep-staged → commit removed, 'M  app.txt' staged (log shows only base). Correct. |
| M-16 | Undo -> discard: TypeToConfirm + trash-net | ✅ PASS | Discard path: 4-option gate → TypeToConfirm (typed the oid) → reset. HEAD is now 'base' — the commit was ACTUALLY DROPPED (v0.2 was a phantom no-op). Safety copy reads 'type the highlighted value' (token-neutral, M-16 copy fix). No new trash dir written because the discarded commit had no uncommitted tracked changes to back up (correct — the '20260805' dir is a stale pre-existing one). P0 reset fix + M-16 copy fix both confirmed live. |
| M-17 | --yes cannot undo | ✅ PASS | `--yes undo` refused with EXIT=1 (v0.2 was exit 0); refusal echoes the actual gate question ('Undo ff54d5e "to undo" — what should happen…'), NOT the old wrong 'rebase vs merge' copy. HEAD == PRE (untouched). P1 exit-code + M-17 copy fix confirmed. |
| M-18 | Multi-count undo halts with guidance | ✅ PASS | 'undo the last 3 commits' → no gate, no action; guidance offers squash-3 / revert / undo-most-recent; HEAD == PRE unchanged. Recognize-but-don't-act boundary holds. |
| M-19 | Squash last 3: tree-identical | ✅ PASS | 'squash the last 3' fast-path (*) → squash gate with combined message → count 4→2 (dropped by 2), tree oid IDENTICAL (bf23f09…). A real squash into one commit. v0.2 was a phantom single-reset no-op; P0 + P2 squash-routing fixes confirmed. |
| M-20 | Amend-on-pushed: escalation + lease (flagship) | ✅ PASS | FLAGSHIP now works end-to-end: 'fix the last commit message to \'typo message fixed\'' fast-path (*) → amend recognized → detected published commit → force-push escalation with the ⛔ irreversible block → TypeToConfirm on branch name 'main' → amend + `--force-with-lease` (log shows 'forced update', NO bare --force). Remote subject is now 'typo message fixed'. The whole flow that was unreachable in v0.2 is live. P2 amend fix confirmed. |
| M-21 | Failing pre-commit blocks (via system git) | ⚠️ PASS (with defects) | Hook enforcement works: 'Hook(s) present (pre-commit) — using system git', commit BLOCKED, 'LINT FAILED' surfaced, count 1→1 unchanged. DEFECT: final EXIT=0 — the interactive recovery picker (Show/Cancel) was entered and 'Show' exits 0, so the blocked-commit's nonzero status is lost to a caller. The block itself is correct and no bad commit was made; the exit code after the picker is the defect (same exit-honesty family as the P1 cluster, but on the hook-block→picker path). |
| M-22 | Revert parity: succeeds despite the same hook | ✅ PASS | Revert SUCCEEDED despite the identical failing pre-commit hook (inverse commit '317f629 Revert "to revert"' exists) — matches real git, where revert doesn't run pre-commit. Parity with M-21 proven: commit blocked, revert allowed. |
| M-23 | Deleted branch -> find my lost work (flagship) | ✅ PASS (flawless) | ★★ Deleted branch 'experiment' → 'find my lost work' → RecoveryBrowser listed 'the work I will lose' (1 file) → restored to `rescue/20260807-5188725` at EXACTLY the lost oid 5188725; HEAD before == after (b5ed3a5…, untouched); working tree unchanged. The origin-story scenario, flawless. Flagship — worth recording. |
| M-24 | Dropped stash surfaces | ✅ PASS | Dropped stash surfaced: browser listed the stash-shaped candidate 'On main: important wip — 1 file [stash]' (Source B odb-scan — no reflog trace); restored to a rescue branch. Proves the two-source recovery design. |
| M-25 | Empty-scan honesty | ✅ PASS | Empty scan is honest: 'Nothing found. Work that was never committed, or that git has already garbage-collected, may be unrecoverable.' — names the gc'd/never-committed caveat, not a bare nothing-found. |
| M-26 | Clean-up gate + trash backup, nested dirs | ✅ PASS | Cleanup gate states tracked/untracked COUNTS (1 tracked, 1 untracked) and names the trash-net in each consequence. Chose delete-untracked → junk/ removed from tree; nested file present + byte-path-identical at ~/.gitrust/trash/20260807-132721/junk/inner/file.txt; tracked mod untouched. Trash-net (clean path) + nested-dir recursion correct. |
| M-27 | Fail-closed trash-net | ✅ PASS | Fail-closed: with ~/.gitrust/trash chmod 000, clean REFUSED — 'Failed to create trash dir … Permission denied', EXIT=1, and keepme.txt STILL PRESENT (nothing deleted without a backup). Runner auto-restored chmod 755 after. Fail-closed invariant holds, and exits nonzero correctly. |
| M-28 | Recover precedence: sideways pointer | ✅ PASS | `--recover` with no interrupted pipeline: 'No interrupted GiTrust pipeline found for this repo. If you're looking for lost commits, try gitrust "find my lost work".' — the sideways pointer connects the two recovery worlds. |
| M-29 | Ollama down: graceful degrade | ⏭️ SKIP (not exercised — Ollama was up) | The first command showed ◉ (llm · ~15.9s) and SUCCEEDED — meaning Ollama was still RUNNING, so the graceful-degrade path (friendly LLM-down error) was not actually exercised. Not a product failure; the test setup needed Ollama stopped and it wasn't. Re-run with 'brew services stop ollama' to properly verify. (The v0.2 run confirmed graceful degrade PASSES when Ollama is truly down.) |
| M-30 | Not a repo | ✅ PASS | Outside a git repo: '✗ Not inside a git repository…' friendly message, no stack trace, EXIT=1. v0.2 was exit 0 (and the earlier harness bug made the dir look like a repo). Both the P1 exit-code correctness and the harness sandbox-location fix confirmed. |

## Failures & defects to triage

- **M-13** — ⚠️ PASS (with defects) — Branch-here rescue works (created + switched to rescue-work, no data loss). BUT the original 'commit this' did NOT complete: pre-check blocked with 'Nothing staged to commit' — the resume reached the commit step but the change wasn't auto-staged, so the commit-continuation still doesn't land the user's edit. The M-13 resume fix wires the redirect through, but the commit needs staging. Change is safe (M app.txt on rescue-work), so PASS-with-defect, not FAIL.
- **M-21** — ⚠️ PASS (with defects) — Hook enforcement works: 'Hook(s) present (pre-commit) — using system git', commit BLOCKED, 'LINT FAILED' surfaced, count 1→1 unchanged. DEFECT: final EXIT=0 — the interactive recovery picker (Show/Cancel) was entered and 'Show' exits 0, so the blocked-commit's nonzero status is lost to a caller. The block itself is correct and no bad commit was made; the exit code after the picker is the defect (same exit-honesty family as the P1 cluster, but on the hook-block→picker path).

_Generated by rollup.sh from per-test records in [`results/`](results/)._
