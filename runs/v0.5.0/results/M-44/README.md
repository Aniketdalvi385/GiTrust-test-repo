# M-44 · 'Pull the latest from origin into this branch' is a pull

| | |
|---|---|
| **Part** | 2 · Divergence |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 16:00 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ still on feature
- ✅ feature has origin/feature's new commit
- ✅ feature does NOT contain main's new commit
- ✅ not routed to 'Update from main'
- ✅ no panic / raw error chain

## What a human should judge

A pull of this branch from its own remote (✦ Pull, or a 'which did you mean?' menu) — never ⚡ 'Update from main' (F3): feature gets origin/feature's new commit, not main's.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS-WITH-NOTES
Summary: F3 is fixed: "pull the latest from origin into this branch" became "✦ Pull from origin", feature got origin/feature's commit and not main's, exit 0. The routing took 31.9s, and the plan line is vague.

- Right: "✦  Pull from origin · 31.9s", never "⚡ Update from main". The 1-step plan ran on Enter with "→ Pulled 1 commit(s) from origin", then "✓ Done · on feature, ↑0 ↓0".
- Slow: "· 31.9s" for one routing decision. Every other model call in this run took 0.7–3.2s, so this is most likely the four shards sharing the model (as the v0.4.1 report found for M-36). Worth a re-check on its own before blaming the product.
- Plan copy (convention 9): "●  pull      from origin" doesn't say which branch or how. Something like "origin/feature into feature (fast-forward)" would be clearer and would confirm right in the plan that this is this branch's own remote, not main.
- Polish: "○  pull      from origin" stays on screen above "✓  pull      from origin" (see M-37), and "Pulled 1 commit(s)" has a lazy plural.
