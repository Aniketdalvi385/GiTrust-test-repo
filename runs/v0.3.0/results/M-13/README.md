# M-13 · Detached write -> rescue

| | |
|---|---|
| **LLM** | yes |
| **Ollama** | on |
| **Result** | ✅ PASS |
| **Run** | v0.3.0 · 2026-08-07 15:10 (re-run after fix) |

## What to look for
Choose BRANCH-HERE. PASS (post-fix) = branch created AND the commit is actually made (not left uncommitted).

## Command
```bash
$GITRUST "commit this"
```

## Notes
FIXED. Branch-here rescue on a dirty detached HEAD now stages the uncommitted edit, so the resumed "commit this" lands. Live: 'Create a branch HERE' → '✓ Created and switched to rescue-work' → '✓ Staged your current changes on rescue-work' → drafted message → 'Committed: … (936ffaa→39c9c94)' → 'Done · 1 commit on rescue-work'. Post-facts confirm HEAD moved (936ffaa→39c9c94) and the working tree is clean — the user's work actually landed, no data loss. The v0.3.0 first-run defect (edit left unstaged → 'Nothing staged to commit') is gone. Regression test: detached_rescue_branch_here_stages_dirty_edit_for_resume.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
