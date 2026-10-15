Verdict: PASS-WITH-NOTES
Summary: Guard warns stranded commit, saves branch first, then switches; menu nits.

- Clear warning: "You have 1 commit(s) here that are on NO branch — switching away now would strand them." A branch is created first (rescue-worksaved-work) and the commit is preserved. Then "Switched to main", exit 0.
- Same menu nits as M-13: a "Cancel" row, unnumbered, and the awkward option "Switch back to your previous branch (no changes made)" which is confusing when the user asked to go to main.
- The branch is created before the plan is confirmed. The default name "rescue-work" was appended to in the harness ("rescue-worksaved-work"), as in M-13.
