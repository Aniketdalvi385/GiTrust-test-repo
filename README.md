# GiTrust — acceptance tests and evals

Release-level testing for [GiTrust](https://github.com/Aniketdalvi385/gitrust): the
experience-level complement to its `cargo test` suite. Does the real binary do the right thing,
say it clearly, refuse safely, exit with the right code, and recover what it promises to?

Each **version** gets a self-contained run under [`runs/`](runs/), so results compare across
releases.

## Runs

| Version | Date | How | Suite result | Eval (whole system) | Report |
|---|---|---|---|---|---|
| [v0.2.0](runs/v0.2.0/) | 2026-07-31 → 08-05 | manual, 31 tests | 19 ✅ · 4 ⚠️ · 8 ❌ | — | [REPORT](runs/v0.2.0/REPORT.md) |
| [v0.3.0](runs/v0.3.0/) | 2026-08-07 → 08-10 | manual + captured, 31 tests + variants | 40 ✅ · 2 ⚠️ · 0 ❌ | — | [REPORT](runs/v0.3.0/REPORT.md) |
| [v0.4.1](runs/v0.4.1/) | 2026-10-15 | automatic (PTY) + agent screen review + ★ by hand, 43 tests | 19 ✅ · 21 ⚠️ · 3 ❌ (+ 4 ★ by hand: 2 ✅ · 2 ⚠️, recorded) | 377 / 450 right, 68 asked, 3 wrong actions | [REPORT](runs/v0.4.1/REPORT.md) |
| [**v0.5.0**](runs/v0.5.0/) | 2026-10-16 → 10-29 | automatic (PTY) + agent screen review + ★ by hand, 48 tests | 20 ✅ · 28 ⚠️ · 0 ❌ (+ 4 ★ by hand: 1 ✅ · 3 ⚠️, all checks pass) | 377 / 450 right, 70 asked, 1 wrong action (stops before acting) | [REPORT](runs/v0.5.0/REPORT.md) |

v0.4 replaced the qwen LLM with the Kev decision model and tightened the conventions (every
back-out exits 1, no Cancel rows, no raw errors), so its ⚠️ count isn't comparable with v0.3's.
The v0.4.1 findings (F1–F20) are in its [REPORT](runs/v0.4.1/REPORT.md#findings); the plan that fixed them lives with the code, in
GiTrust's [`docs/v0.5.0_fix_plan.md`](https://github.com/Aniketdalvi385/gitrust/blob/main/docs/v0.5.0_fix_plan.md).
v0.5.0 closes all 20 and 11 more found on the way (F21–F31); its [REPORT](runs/v0.5.0/REPORT.md) has
what's left. The suite holds the v0.5.0 expectations (M-43…M-47 new, 22 tests updated);
the v0.4.1 run's are in git history — see [suite/README.md → Versions](suite/README.md#versions).

## Layout

```
suite/                 the acceptance suite (Python) — start with suite/README.md
  tests.py               48 tests as data: setup, keys to press, checks (v0.5.0 expectations)
  gitrust_suite.py       fixtures (scratch HOME + bare remote), the PTY driver, records
  run.py                 auto | manual | list
  rollup.py              builds runs/vX/README.md from the records
eval/                  the eval: what GiTrust DOES with a request, through the binary
  run_eval.py            gitrust --yes "<request>" in a throwaway repo, per request
  sets/                  v1_44, v2_owner_68, v3_blind (+ the raw persona/annotator files)
runs/vX.Y.Z/
  README.md              index: every test, verdict, one-line note; eval table
  REPORT.md              the narrative: method, results, findings
  results/M-NN/          README.md · screens.txt · result.json · review.md (· session-N.txt)
  eval/                  per-set rows (every request, outcome, output on misses) + summary
  evidence/              screen recordings of the ★ flagship tests
legacy/                the v0.2/v0.3 bash runner and 31-test document (kept for those runs)
```

## Running a release

```bash
# 0. build the binary and start the model it ships with
(cd ../Glit/gitrust && cargo build --release)
(cd ../Glit && KEV_DIR=../kev ./docs/classifier_eval/kevctl.sh start AniketDalvi385/gitrust-kev-0.8b@v2)

# 1. the suite, automatically (4 parallel shards ≈ 10 min)
for i in 0 1 2 3; do uv run --with pyte python suite/run.py auto 0.5.0 --shard=$i/4 & done; wait

# 2. review the screens (an agent or you): write results/<id>/review.md
#    "Verdict: PASS | PASS-WITH-NOTES | FAIL" + "Summary: …" + notes

# 3. the flagship tests by hand, recorded
python3 suite/run.py manual 0.5.0 M-06

# 4. the eval (≈ 15 min), then the index
python3 eval/run_eval.py 0.5.0
python3 suite/rollup.py 0.5.0
```

Everything runs in throwaway directories with a scratch `HOME`; your real `~/.gitrust.toml`,
`~/.gitrust/` and repositories are never touched. Sandboxes are not committed.

## The eval sets

| Set | n | Written by | Notes |
|---|---|---|---|
| `v1_44` | 44 | the 2026-08 classifier research | the paper's set; one strict label each |
| `v2_owner_68` | 68 | the owner, 2026-10-14 | answers to 31 situations; never trained on |
| `v3_blind` | 338 | three persona agents, 2026-10-15 | saw only operation descriptions, never training data; independently re-labelled (338/338 agree); near-duplicates of training phrasings removed |

None of these may be used for training. Adding to the eval: write new requests to a new
`sets/vN_*.json` (`{"cases": [{"id", "q", "accept": [ops], "situation"}]}`), run the near-duplicate
filter against the training data first, and keep the set's provenance in its `about` field.
