# M-32 · q at the plan cancels; stray keys are ignored

| | |
|---|---|
| **Part** | 8 · UX |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:53 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 1
- ✅ screen shows 'Canceled'
- ✅ nothing committed
- ✅ no panic / raw error chain

## What a human should judge

A stray key does nothing; q cancels; exit 1.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS
Summary: Stray key ignored, q cancels with exit 1, nothing committed.

- Plan screen shown after the message prompt; the stray key left it unchanged and q produced "↪  Canceled — nothing was done." exit 1.
- Message was pre-filled from the request ("not this time"), so Enter-to-accept was correct.
- Minor: "commit ... ⚠" warning marker is unexplained on the plan; consistent across tests so not a defect.
