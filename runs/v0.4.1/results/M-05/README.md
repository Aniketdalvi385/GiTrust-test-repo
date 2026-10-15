# M-05 · Create a branch; dirty switch is handled

| | |
|---|---|
| **Part** | 1 · Everyday |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 18:01 |
| **Automatic checks** | ❌ failed |

## Checks

- ✅ branch created (exit 0)
- ✅ feature-x exists
- ✅ the uncommitted edit survives the switch attempt
- ✅ a refused switch does not exit 0
- ✅ no panic / raw error chain
- ❌ no panic / raw error chain — `caused by:`

## What a human should judge

Branch created; switching back with uncommitted edits either works safely or is refused with a clear reason — never a crash, never lost edits.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: FAIL
Summary: Branch created; dirty switch is safe but shows a raw libgit2 error chain.

- `create branch feature-x` → one-step plan, "Created branch feature-x", exit 0.
- `switch to other` with an uncommitted edit to app.txt that the switch would overwrite: the edit survives and the run exits non-zero — the behaviour is safe.
- But the message is libgit2's: "✗  Failed to checkout 'other'" / "caused by: 1 conflict prevents checkout; class=Checkout (20); code=Conflict (-13)", printed twice. No plain explanation and no next step (commit or `gitrust "stash"` first). Same class as F2 (raw error chains). Reviewed by hand (the automatic check caught it).
