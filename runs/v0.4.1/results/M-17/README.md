# M-17 · --yes cannot undo

| | |
|---|---|
| **Part** | 4 · Undo |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:39 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 1
- ✅ HEAD untouched
- ✅ screen shows 'Choices'
- ✅ no panic / raw error chain

## What a human should judge

Refuses to choose for you, lists the choices, exit 1.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS
Summary: --yes refuses to pick an undo mode, lists choices, exits 1.

- Message: "✗  --yes won't choose for you — Undo f143c04 "feat: the mistake" — what should happen to its changes?" then lists all four choices and "Run it interactively (without --yes) to pick one, or say more precisely what you want." Plain and actionable.
- Exit 1, HEAD untouched. No panic or raw chain.
- Minor: first line uses "*" instead of ⚡/✦/◇ (probably a no-tty variant of the marker). The choice list also carries the "⚠⚠" glyph inline.
