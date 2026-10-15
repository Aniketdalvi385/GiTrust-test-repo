Verdict: PASS
Summary: Lists lost commit in plain words, restores to a rescue branch safely.

- "Lost & recoverable commits (restoring creates a rescue branch — your current work is never touched):" then a numbered menu, "[1] just now — 'the work I'll lose' — 1 file". The list is plain and has no Cancel row.
- Result: "Recovered 63f6839 onto new branch `rescue/20261015-63f6839`. Your current branch and files are unchanged." Rescue branch is at the lost commit, HEAD untouched, exit 0.
- A one-item menu is fine. It still asks for a pick, which is safe.
