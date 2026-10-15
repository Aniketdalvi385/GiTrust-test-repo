# M-04 · Scoped push: only the login files

| | |
|---|---|
| **Part** | 1 · Everyday |
| **Model** | yes |
| **Flagship** | ★ yes |
| **Run** | auto · 2026-10-15 17:50 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ login.txt pushed
- ✅ readme.txt NOT pushed
- ✅ readme.txt still uncommitted
- ✅ no panic / raw error chain

## What a human should judge

Picker pre-selects the login files, shows +N −M and a reason per file; readme.txt not pre-selected; only login files reach the remote.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS
Summary: Picker pre-selects login files; only they were committed and pushed.

- Picker: "2 of 3 changed files pre-selected", auth_login.txt and login.txt are [x] with "+1  new · name matches “login”"; readme.txt is [ ] with "might be part of “login” — your call". Matches the README expectation.
- An empty commit message was rejected with "# This can't be empty — type a value, or press Esc to cancel." Good.
- The plan shows stage, commit "login page" and push, with "[s] don't push". The result is "Pushed 1 commit(s) to origin/main", and the undo hint says "(reverts it — it's pushed)". Excellent.
- Note: the first line is ⚡ for an interpreted phrase, with no ✦ time. Possibly an alias or exact route; not a problem.
