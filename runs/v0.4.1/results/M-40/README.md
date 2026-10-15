# M-40 · Clean tree: 'commit everything' stops before asking

| | |
|---|---|
| **Part** | 8 · UX |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:43 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ screen shows 'Nothing to commit'
- ✅ screen never shows 'message'
- ✅ no panic / raw error chain

## What a human should judge

Says nothing to commit before any message prompt.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS-WITH-NOTES
Summary: Clean tree stops before any prompt, exit 1; piped marker is "*".

- "✗  Nothing to commit — the working tree is clean." Printed with no message prompt, exit 1 (did nothing, so not 0). Correct and clear.
- First line "*  Commit everything" uses ASCII "*" in pipe mode rather than ⚡; same minor deviation as other piped runs.
