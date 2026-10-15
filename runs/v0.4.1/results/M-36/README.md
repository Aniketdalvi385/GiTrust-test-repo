# M-36 · Not a Git request: refused, exit 1

| | |
|---|---|
| **Part** | 8 · UX |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:39 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 1
- ✅ screen shows "doesn't look like a Git request"
- ✅ no panic / raw error chain

## What a human should judge

A polite refusal pointing at `gitrust help`.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS-WITH-NOTES
Summary: Polite refusal with exit 1, but took 14.3s to decide.

- "✗  That doesn't look like a Git request. Try e.g. "show status" or "push my commits" — or `gitrust help` for phrases that always work." Polite, specific, exit 1.
- No first understood-line (✦) is shown for the refusal; acceptable.
- 14.3s before refusing is slow compared with 1-4s elsewhere (likely model cold/slow); worth a look. The mid-word wrap ("p / hrases") is a test-terminal width artifact.
