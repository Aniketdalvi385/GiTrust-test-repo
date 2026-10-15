# M-30 · Not a repository

| | |
|---|---|
| **Part** | 7 · Meta |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:18 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ non-zero exit
- ✅ no panic / raw error chain

## What a human should judge

Friendly not-a-repo message, exit ≠ 0.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS-WITH-NOTES
Summary: Friendly not-a-repo message with exit 1; piped first line uses "*" marker.

- "✗  Not inside a git repository. Run 'gitrust "initialize a repository"' or 'git init' first." is plain, specific and exits 1.
- First line is "*  Show status" rather than "⚡  Show status". Piped runs appear to use an ASCII "*" in place of the ⚡/✦ markers; harmless, but a small deviation from the stated convention (applies to all pipe runs).
