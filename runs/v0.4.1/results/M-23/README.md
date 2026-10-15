# M-23 · Deleted branch → find my lost work

| | |
|---|---|
| **Part** | 6 · Forensics |
| **Model** | no |
| **Flagship** | ★ yes |
| **Run** | auto · 2026-10-15 17:17 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ a rescue branch exists
- ✅ rescue branch at the lost commit
- ✅ HEAD untouched
- ✅ no panic / raw error chain

## What a human should judge

Lists the lost commit in plain words; restores it to a rescue branch; your current branch and files untouched.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS
Summary: Lists lost commit in plain words, restores to a rescue branch safely.

- "Lost & recoverable commits (restoring creates a rescue branch — your current work is never touched):" then a numbered menu, "[1] just now — 'the work I'll lose' — 1 file". The list is plain and has no Cancel row.
- Result: "Recovered 63f6839 onto new branch `rescue/20261015-63f6839`. Your current branch and files are unchanged." Rescue branch is at the lost commit, HEAD untouched, exit 0.
- A one-item menu is fine. It still asks for a pick, which is safe.
