# M-35 · Learned phrase: a menu pick is instant next time

| | |
|---|---|
| **Part** | 8 · UX |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:17 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ screen shows 'learned'
- ✅ learned run exits 0
- ✅ screen shows 'whats goin on'
- ✅ forget exits 0
- ✅ no panic / raw error chain

## What a human should judge

Second run says '· learned' and works with the model down; `aliases` lists it.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS
Summary: Unclear phrase got a menu; pick learned, instant offline next time.

- "whats goin on" produced "That may not be a Git request. If it is, which operation did you mean?" with 3 numbered choices (model asked a menu rather than acting - safe). Pick printed "↳ Learned “whats goin on” → Show status · instant next time (gitrust aliases)", then "◇  Show status · your choice".
- Second run with model down: "⚡  Show status · learned", exit 0, 0.0s. `aliases` lists it; --forget removes it ("Forgot “whats goin on”."). All as designed.
- Minor ordering: the "↳ Learned" line prints before the "◇" first line, so the run does not open with the understood-line; slightly odd but readable.
