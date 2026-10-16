# M-21 · A failing pre-commit hook blocks the commit

| | |
|---|---|
| **Part** | 5 · Hooks |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 11:25 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 1
- ✅ screen shows 'LINT FAILED'
- ✅ the hook's output is shown once
- ✅ no new commit
- ✅ the files are still staged
- ✅ no menu after the failure (F8)
- ✅ the screen says the files are still staged
- ✅ never says 'nothing was done' (the files were staged)
- ✅ no snapshot / --recover advice when only staging ran (F8)
- ✅ no panic / raw error chain

## What a human should judge

Says hooks were detected; the hook's output is shown once; then a plain message — no menu (D7): the files are still staged, fix what the hook reported and commit again; nothing committed; exit 1; never 'nothing was done'; no snapshot/--recover lines for a failure that only staged files.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
