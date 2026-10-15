# M-38 · No terminal, a question needed: plain message, exit 1

| | |
|---|---|
| **Part** | 8 · UX |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:19 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 1
- ✅ screen shows 'no terminal to ask in'
- ✅ no panic / raw error chain

## What a human should judge

One readable line, no 'caused by'.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS-WITH-NOTES
Summary: One plain line, exit 1; piped first line shows "*" not ⚡.

- "✗  This needs an answer, and there's no terminal to ask in (input or output is redirected). Run it in a terminal — or, in a script, say it precisely enough to need no choice and add --yes." One readable line, no "caused by", exit 1.
- Minor: the advice "add --yes" is misleading for undo, since --yes never picks an option (M-29 says so). Also the "*  Undo the last commit" marker is ASCII in pipe mode instead of ⚡.
