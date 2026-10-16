# M-05 · Create a branch; dirty switch is handled

| | |
|---|---|
| **Part** | 1 · Everyday |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 11:25 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ branch created (exit 0)
- ✅ feature-x exists
- ✅ the uncommitted edit survives the switch attempt
- ✅ the blocked switch exits 1
- ✅ the switch is blocked before any plan
- ✅ screen says 'would overwrite your uncommitted changes to app.txt'
- ✅ switching to the current branch exits 0 (D4: the end state holds)
- ✅ screen says 'Already on main.'
- ✅ still on main
- ✅ no panic / raw error chain
- ✅ no panic / raw error chain
- ✅ no panic / raw error chain

## What a human should judge

Branch created. Switching with an edit the switch would overwrite is blocked before any plan, naming the file and the way out (commit or stash) — never a raw libgit2 error, never lost edits (F18). Switching to the branch you're on says so (F17).

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
