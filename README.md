# GiTrust — Manual Acceptance Test Records

Human-eyes acceptance testing for the GiTrust release binary — the experience-level complement to
the automated `cargo test` suite. It verifies the *experience*: gates render right, copy reads
right, refusals feel right, destructive ops are safe, recovery actually recovers.

Each **version** gets its own self-contained run under [`runs/`](runs/), so results are comparable
across releases as bugs get fixed and the tool moves toward public release.

## Runs

| Version | Date | Result | Report |
|---|---|---|---|
| [**v0.2.0**](runs/v0.2.0/) | 2026-07-31 → 08-05 | 19 ✅ · 4 ⚠️ · 8 ❌ | [REPORT](runs/v0.2.0/REPORT.md) |
| [**v0.3.0**](runs/v0.3.0/) | 2026-08-07 | 31 ✅ · 0 ⚠️ · 0 ❌ · 0 ⏭️ | [REPORT](runs/v0.3.0/REPORT.md) |

**Public-release gate:** all 🔴 critical/systemic findings resolved and a clean re-run (0 ❌) before
the tool goes public. v0.2.0 surfaced three root-cause clusters (below) — v0.3.0 re-runs the same
31-test suite to verify the fixes.

## Open root-cause clusters (from v0.2.0 — must clear before public)

1. **🔴 Systemic exit-code bug** — every non-success path returns exit 0 (7× confirmed). Makes the CLI unsafe to script.
2. **🔴 Reset execution path is a phantom op** — `reset --hard`/`--soft` report success while HEAD never moves; M-16 also claims a trash backup never written. (Trash-net module itself is proven sound — bug is the reset executor.)
3. **Argument/target extraction** — requests carrying a target/scope/argument get dropped or misrouted (scope, branch names, sync target, squash count, amend).

Full detail, evidence, and the "what works well / keep" list are in each run's REPORT.

## Repo layout

```
GiTrust-test/
  README.md              ← this cross-version dashboard
  MANUAL_TEST_SUITE.md   ← the 31-test suite (shared reference, all versions)
  harness.sh  run.sh     ← test harness + output-capture helper (source once per terminal)
  runs/
    v0.2.0/
      README.md          ← this run's index (env + results table)
      REPORT.md          ← this run's summary (verdicts, root causes, keep-list)
      results/M-00…M-30/ ← per-test: README (findings) + commands.sh + output.log
      evidence/          ← flagship screen recordings (.mov)
  sandboxes/             ← throwaway per-test git repos (git-ignored, never pushed)
```

## Running a new version's suite

1. Build the new release binary; point `harness.sh`'s `$GITRUST` at it, bump the version note.
2. `mkdir -p runs/vX.Y.Z/{results,evidence}` and copy the empty results scaffold (or re-generate).
3. `source harness.sh && source run.sh`, then work through `MANUAL_TEST_SUITE.md` M-00 → M-30,
   filling each `runs/vX.Y.Z/results/M-NN/README.md`.
4. Write `runs/vX.Y.Z/REPORT.md` and add a row to the **Runs** table above.

Tests run against a **local throwaway bare remote** per case (under `sandboxes/`, git-ignored — never pushed).
Only the records in each run's `results/` and `evidence/` are committed.
