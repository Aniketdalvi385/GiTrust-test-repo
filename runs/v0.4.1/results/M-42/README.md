# M-42 · Help lists only phrases that work instantly

| | |
|---|---|
| **Part** | 8 · UX |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:39 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ 'log' works with the model down
- ✅ 'branches' works with the model down
- ✅ 'current branch' works with the model down
- ✅ 'remotes' works with the model down
- ✅ 'config' works with the model down
- ✅ 'diff' works with the model down

## What a human should judge

Look-section phrases from help all work with the model down.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS
Summary: Every Look-section phrase in help works instantly with the model down.

- Help lists "status · log · diff · show · branches · remotes · config"; log, branches, current branch, remotes, config and diff all ran exit 0 in 0.0s with the model down.
- Help states Esc cancels and that --yes never picks for you; matches conventions.
- Notes: piped runs show "*" instead of ⚡; "current branch" shows "List branches" (the whole list, not just the current name), acceptable.
