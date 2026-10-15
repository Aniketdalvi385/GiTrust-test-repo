# M-37 · Commit and push in one request

| | |
|---|---|
| **Part** | 8 · UX |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:40 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ screen shows 'Commit and push'
- ✅ pushed (0 0)
- ✅ subject
- ✅ no panic / raw error chain

## What a human should judge

✦ Commit and push everything; asks for the message; pushed.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS
Summary: "commit n push" routed by the model; message asked, committed and pushed.

- "✦  Commit and push everything · 1.0s", then "? Commit message:" prompt, plan with 3 steps and legend including "[s] don't push".
- Result: Committed 6d038ce→fdf2b8d, "Pushed 1 commit(s) to origin/main", "↑0 ↓0", exit 0. Next line warns undo "reverts it — it's pushed", a nice touch.
