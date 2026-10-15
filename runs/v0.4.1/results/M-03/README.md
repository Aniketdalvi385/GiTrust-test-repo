# M-03 · Commit: the message is yours, [e] edits it

| | |
|---|---|
| **Part** | 1 · Everyday |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:52 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ commit subject is the edited text
- ✅ tree clean afterwards
- ✅ no panic / raw error chain

## What a human should judge

GiTrust asks for the message (never drafts one); the plan shows it; `e` edits it.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS
Summary: Message asked from user, shown in plan, [e] edit works, committed.

- "⚡  Commit everything" then "? Commit message:" with an empty field. GiTrust does not draft a message. Correct.
- The plan shows "commit "first try"  ⚠"; [e] reopens the prompt pre-filled and the plan updates to "my message".
- The result is "Committed: my message (02f8984→3b7d40a)" with the Next/undo hint, exit 0.
- Minor: the "⚠" on stage/commit steps is never explained on screen.
