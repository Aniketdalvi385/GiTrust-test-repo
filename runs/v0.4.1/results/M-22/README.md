# M-22 · Revert succeeds despite the same hook

| | |
|---|---|
| **Part** | 5 · Hooks |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:51 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ one new (revert) commit
- ✅ other.txt gone
- ✅ no panic / raw error chain

## What a human should judge

Matches git: revert doesn't run pre-commit, so it succeeds. Note: revert asks its own (Y/n) question instead of the one-key plan prompt every other operation uses.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS-WITH-NOTES
Summary: Revert works with exit 0, but uses its own Y/n question plus plan Enter.

- Prompt "? Revert a7ec361 with a new inverse commit? (Y/n)" is followed by the plan "[Enter] run · [q] cancel". This is a double confirmation and a different key style from other operations (Y/n vs one-key plan).
- Raw git output leaks into the step line: `○  revert    a7ec361[main 4fe1afd] Revert "to be reverted"` / " delete mode 100644 other.txt".
- Behaviour right: one revert commit, other.txt gone, "Reverted a7ec361 (inverse commit added)", exit 0. Not blocked by the pre-commit hook, which matches git.
- The prompt names the SHA but not the commit message, so the user has to know what a7ec361 is.
