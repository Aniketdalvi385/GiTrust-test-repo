# M-24 · A dropped stash surfaces

| | |
|---|---|
| **Part** | 6 · Forensics |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:39 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ rescue branch has the wip change
- ✅ no panic / raw error chain

## What a human should judge

The dropped stash is listed and can be restored to a branch.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS-WITH-NOTES
Summary: Dropped stash is listed and restored; an internal index entry adds noise.

- The menu shows "[1] just now — 'On main: important wip' — 1 file [stash]", marked as a stash. Choosing it gives "Recovered 95e221b onto new branch `rescue/20261015-95e221b`." Rescue branch has the wip change, exit 0.
- Row 2 is "'index on main: 638d1bf base' — 0 files", an internal stash-index commit with no content. It is confusing and offers nothing worth restoring. Filter it out or fold it under the stash.
- "just now" is vague for ordering several items. A time would help.
