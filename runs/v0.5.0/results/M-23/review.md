Verdict: PASS
Summary: The lost commit is listed in plain words and restored to a rescue branch; current branch and files untouched; exit 0.

- "⚡  Find lost work", then "Lost & recoverable commits (restoring creates a rescue branch — your current work is never touched):" over a numbered menu — "[1] just now — 'the work I'll lose' — 1 file" — with "Esc cancel" in the help line and no Cancel row. The header says what a pick does, so the pick is the one confirmation; the only change is a new branch.
- "Recovered 55cb395 onto new branch `rescue/20261016-55cb395`. Your current branch and files are unchanged." — true: the rescue branch is at the lost commit, HEAD untouched; exit 0.
- v0.4.1 notes: plain, numbered list without a Cancel row — still. Result line, rescue branch, exit 0 — still. One-item menu still asks for a pick — still, and fine.
