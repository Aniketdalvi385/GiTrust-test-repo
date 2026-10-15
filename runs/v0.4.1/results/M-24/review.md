Verdict: PASS-WITH-NOTES
Summary: Dropped stash is listed and restored; an internal index entry adds noise.

- The menu shows "[1] just now — 'On main: important wip' — 1 file [stash]", marked as a stash. Choosing it gives "Recovered 95e221b onto new branch `rescue/20261015-95e221b`." Rescue branch has the wip change, exit 0.
- Row 2 is "'index on main: 638d1bf base' — 0 files", an internal stash-index commit with no content. It is confusing and offers nothing worth restoring. Filter it out or fold it under the stash.
- "just now" is vague for ordering several items. A time would help.
