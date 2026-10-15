# M-02 · Model classification of a read-only request

| | |
|---|---|
| **Part** | 1 · Everyday |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:52 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ routed to history or status
- ✅ no model probability shown
- ✅ no panic / raw error chain

## What a human should judge

✦ line names what was understood with a time; output is history or status.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS
Summary: Model asked a which-did-you-mean menu; chosen history ran correctly.

- The model did not act directly. It showed "? I am not sure which operation you meant. Which one?" with 3 numbered options (history, status, remote check) and an Esc-cancel help line. This is correct, safe behaviour.
- No Cancel row, no probabilities. The result line is "◇  Show history · your choice", which fits the convention, and the exit is 0.
- "↳ Learned “anything new in my repo” → Show history · instant next time (gitrust aliases)" is transparent. Saving it is arguably debatable, since "anything new" reads more like status, but it is read-only and visible.
- No ✦ line appeared because the menu was shown. The automatic PASS is fair.
