# Automated test runner

Three scripts turn the 31-test manual suite ([`MANUAL_TEST_SUITE.md`](MANUAL_TEST_SUITE.md))
into a **guided, captured** run — you still watch and drive every gate and make every
verdict, but all the setup, capture, and paperwork is automated.

| Script | Role |
|---|---|
| [`tests.manifest.sh`](tests.manifest.sh) | the 31 tests as data (setup / command / post-facts / notes). Edit here if the suite changes. |
| [`runner.sh`](runner.sh) | the interactive driver — scaffolds the run folder, does each test's setup, runs the command **live with the terminal attached** so you drive gates, captures the session, shows post-facts, asks you for the verdict, writes the per-test record. |
| [`rollup.sh`](rollup.sh) | after a run, generates the version's `README.md` (index) + `REPORT.md` (summary) from the per-test verdicts. |

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
2. runs the setup (creates a throwaway sandbox with a local bare remote);
3. runs the gitrust command **live** — you drive the gates and watch real output;
4. prints deterministic post-facts (HEAD moved? tree oid? exit code? file counts?) to inform your call — **these never decide the verdict for you**;
5. asks: `p`=PASS `f`=FAIL `w`=PASS-with-defects `b`=BLOCKED `s`=SKIP, plus a one-line note;
6. writes `runs/v0.3.0/results/M-NN/README.md` + `commands.sh` + `output.log`.

## Roll it up

```bash
./rollup.sh 0.3.0
```

Generates `runs/v0.3.0/README.md` (environment table + 31-row index) and
`REPORT.md` (verdict summary + failures-to-triage). Then add a row to the
top-level [README](README.md) Runs table.

## Notes

- Sandboxes live under `sandboxes/` (git-ignored) and are recreated per test.
- Flagship demos (M-04, M-06, M-08, M-14, M-20, M-23) are worth screen-recording
  into `runs/vX.Y.Z/evidence/` — the runner doesn't record video.
- The runner never auto-adjudicates. It records exactly the verdict you type — this
  suite is the human-eyes complement to `cargo test`, by design.
