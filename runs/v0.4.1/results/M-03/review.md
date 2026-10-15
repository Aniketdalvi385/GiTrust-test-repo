Verdict: PASS
Summary: Message asked from user, shown in plan, [e] edit works, committed.

- "⚡  Commit everything" then "? Commit message:" with an empty field. GiTrust does not draft a message. Correct.
- The plan shows "commit "first try"  ⚠"; [e] reopens the prompt pre-filled and the plan updates to "my message".
- The result is "Committed: my message (02f8984→3b7d40a)" with the Next/undo hint, exit 0.
- Minor: the "⚠" on stage/commit steps is never explained on screen.
