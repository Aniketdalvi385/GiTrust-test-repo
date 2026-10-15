# Automated test runner

Three scripts turn the 31-test manual suite ([`MANUAL_TEST_SUITE.md`](MANUAL_TEST_SUITE.md))
into a **guided, captured** run — you still watch and drive every gate and make every
verdict, but all the setup, capture, and paperwork is automated.

| Script | Role |
|---|---|
| [`tests.manifest.sh`](tests.manifest.sh) | the 31 tests as data (setup / command / post-facts / notes). Edit here if the suite changes. |
| [`runner.sh`](runner.sh) | the capture-only driver — scaffolds the run folder, does each test's setup, runs the command **live with the terminal attached** so you drive the gates, and captures the session + post-facts to `results/M-NN/output.log`. It does **not** ask for a verdict (records are written PENDING). |
| [`rollup.sh`](rollup.sh) | after adjudication, generates the version's `README.md` (index) + `REPORT.md` (summary) from the per-test verdicts. |

**Division of labor:** you drive the gates (the judgment steps); **Claude adjudicates** — reads the captured `output.log`s, writes each verdict + notes into the per-test README, then runs the roll-up. You never type verdicts into the script.

## Prerequisites

- Rebuild the binary for the version under test and confirm `gitrust --version`:
  ```bash
  (cd ../Glit/gitrust && cargo build --release)
  ```
  The `GITRUST` path is set in [`harness.sh`](harness.sh); the runner warns if
  `--version` doesn't match the run folder.
- Ollama: the runner pauses and tells you to `brew services stop/start ollama` for
  the tests that need it off (M-01, M-29) or on (everything else).

## Run it

```bash
./runner.sh 0.3.0                 # the whole suite -> runs/v0.3.0/
./runner.sh 0.3.0 M-05            # one test
./runner.sh 0.3.0 M-04 M-10 M-20  # a subset
./runner.sh 0.3.0 --from M-15     # resume from M-15 to the end
```

For each test the runner:
1. prints what to watch for, and nudges Ollama on/off if needed;
2. runs the setup (creates a throwaway sandbox with a local bare remote, in `$TMPDIR/gitrust-sandboxes` — outside any git repo);
3. runs the gitrust command **live** — you drive the gates and watch real output;
4. runs the deterministic post-facts (HEAD moved? tree oid? exit code? file counts?) and captures them;
5. saves the whole session + post-facts to `results/M-NN/output.log` (+ `commands.sh`), writes a PENDING record, and moves on — **no verdict typed**.

## Adjudicate (Claude)

When the run (or a batch) finishes, tell Claude:

```
adjudicate v0.3.0            # or: adjudicate v0.3.0 M-04 M-10 M-20
```

Claude reads each `results/M-NN/output.log`, decides PASS / FAIL / PASS-with-defects
/ BLOCKED, writes the verdict + a findings note into that test's `README.md`, then
runs `./rollup.sh 0.3.0` to generate `runs/v0.3.0/README.md` (index) + `REPORT.md`
(summary) and adds a row to the top-level [README](README.md) Runs table.

## Variants (multi-phrasing / multi-scope tests)

A classification/scoping test often exercises **one behavior** through **many
phrasings** — "push the login changes" vs "push all docs changes" vs "push all
api changes". Those tests declare `T_VARIANTS` in the manifest and fan out into
**sub-records**: `M-04` becomes `M-04a` (login), `M-04b` (docs), `M-04c` (api),
`M-04d` (schema) — each with its own sandbox, `output.log`, and verdict.

Tests currently carrying variants:

| Base | What varies | Sub-records |
|---|---|---|
| **M-03** | commit-phrasing (`commit this` / `save my changes` / `commit everything`) | M-03a–c |
| **M-04** | feature scope (login / docs / api / schema) | M-04a–d |
| **M-10** | sync target phrasing (`sync with main` / `update … from main` / `pull main into feature`) | M-10a–c |
| **M-19** | squash count (`3` / `three` / `combine … into one`) | M-19a–c |
| **M-20** | amend-message phrasing (`fix … to` / `reword … to` / `change … message to`) | M-20a–c |

Running a base id runs **all its variants** in sequence:

```bash
./runner.sh 0.3.1 M-04          # runs M-04a, M-04b, M-04c, M-04d
./runner.sh 0.3.1 M-04 M-10     # all variants of both
```

Adjudicating uses the sub-ids (Claude reads each variant's `output.log` and
writes each `results/M-04a/README.md`, …). The roll-up lists every sub-record as
its own row and counts each toward the totals. A test with no `T_VARIANTS` runs
as a single record exactly as before.

**Adding a variant:** in the test's manifest function, call
`variant <suffix> <label> <SETUP> <CMD> <CHECK>` — the SETUP must name its own
sandbox (`mk_sandbox m04e`). See `t_M_04` for the pattern.

## Notes

- Sandboxes live under `sandboxes/` (git-ignored) and are recreated per test.
- Flagship demos (M-04, M-06, M-08, M-14, M-20, M-23) are worth screen-recording
  into `runs/vX.Y.Z/evidence/` — the runner doesn't record video.
- The runner never auto-adjudicates. It records exactly the verdict you type — this
  suite is the human-eyes complement to `cargo test`, by design.
