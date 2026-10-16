Verdict: PASS
Summary: The dropped stash is listed on its own, without git's internal "index on …" row, and restored to a rescue branch holding the wip change; exit 0.

- One row: "[1] just now — 'On main: important wip' — 1 file [stash]" — numbered, tagged as a stash, no Cancel row, "Esc cancel" in the help line.
- "Recovered 2020732 onto new branch `rescue/20261016-2020732`. Your current branch and files are unchanged." — the rescue branch holds the wip change; exit 0.
- v0.4.1 notes: stash listed and restored — still. Row "'index on main: 638d1bf base' — 0 files" — fixed (the stash row is the only row). "just now" vague for ordering several items — unchanged, but with one item there is nothing to order here.
