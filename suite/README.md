# The acceptance suite — how to run it

One Python definition per test ([`tests.py`](tests.py)) — the expectations of the release
under test, now **v0.5.0** (see [Versions](#versions)) — run two ways by [`run.py`](run.py)
on top of [`gitrust_suite.py`](gitrust_suite.py).

| Mode | Who drives the prompts | Use it for |
|---|---|---|
| `auto` | a pseudo-terminal (pyte) presses the keys the test lists | every test, every release — agents run this |
| `manual` | you, live in your terminal (recorded with `script`) | the ★ flagship tests you want to see and record yourself |

Both modes set up the same throwaway world for each test: a scratch `HOME` (its own
`.gitconfig`, `.gitrust.toml` with `kev_autostart = false`, and `.gitrust/trash`), a bare
remote and a clone. Your real `~/.gitrust.toml` and `~/.gitrust/` are never touched.
After the run, the same checks run on the exit code, the repository and the screen, and
the record is written to `runs/v<version>/results/<id>/`:

```
README.md     title, checks ✅/❌, what a human should judge, review notes
screens.txt   every screen, step by step (auto) or the session transcript (manual)
result.json   checks, exit codes, timings
review.md     the reviewer's verdict and notes (agent or you) — optional
session-N.txt manual mode only: the raw recording
```

## Before a run

1. Build the binary: `cd ../Glit/gitrust && cargo build --release` (or set `GITRUST_BIN`).
2. Start the model the release uses (tests marked `model` need it):
   ```bash
   cd ../Glit && KEV_DIR=../kev ./docs/classifier_eval/kevctl.sh start AniketDalvi385/gitrust-kev-0.8b@v2
   ```
   Model-down tests point at a dead port themselves; no need to stop the server.

## Run

```bash
python3 suite/run.py list                                        # ids, ★ flagship, model, titles
uv run --with pyte python suite/run.py auto 0.5.0                # everything (~15 min)
uv run --with pyte python suite/run.py auto 0.5.0 M-06 M-23      # some
uv run --with pyte python suite/run.py auto 0.5.0 --shard=0/4    # 1 of 4 parallel shards
python3 suite/run.py manual 0.5.0 M-06                           # a flagship, by hand
python3 suite/rollup.py 0.5.0                                    # rebuild runs/v0.5.0/README.md
python3 eval/run_eval.py 0.5.0                                   # the eval (see ../eval/)
```

In **manual** mode the runner prints what to watch for and which prompts to expect, waits
for Enter, then hands you the terminal. Answer the prompts as a user would (the expected
choice is in the test's `watch` line). The checks then run as usual and the recording is
saved next to the auto results. To record the screen for the README, start QuickTime /
`asciinema rec` before pressing Enter and drop the file in `runs/v<version>/evidence/`.

## Versions

`tests.py` holds the expectations of the release under test — now **v0.5.0**, written from
GiTrust's [`docs/v0.5.0_fix_plan.md`](https://github.com/Aniketdalvi385/gitrust/blob/v0.5.0-fixes/docs/v0.5.0_fix_plan.md)
(decisions D1–D9 as accepted) before the fixes landed. When a release changes what is
expected, the tests change in place and keep their ids, so results still compare across
versions (`since` says which version added a test). The expectations a past run was checked
against stay in git history:

| Run | Suite commit | Tests file |
|---|---|---|
| v0.4.1 | `a7d10ed` | `suite/tests_v04.py` |
| v0.5.0 on | `suite_commit` in `runs/v<version>/environment.json` (written by every run) | `suite/tests.py` |

To re-run an older release exactly as it was checked, check out its suite commit and point
it at a build of that release:

```bash
git worktree add ../GiTrust-test-v0.4.1 a7d10ed
(cd ../Glit && git worktree add ../gitrust-0.4.1 v0.4.1 && cd ../gitrust-0.4.1/gitrust && cargo build --release)
cd ../GiTrust-test-v0.4.1
GITRUST_BIN="$(realpath ../gitrust-0.4.1/gitrust/target/release/gitrust)" \
  uv run --with pyte python suite/run.py auto 0.4.1-rerun     # GITRUST_BIN must be absolute
```

A `suite_commit` ending in `+edits` means `suite/` had uncommitted changes during the run —
commit the suite before a release run so the run can be reproduced.

## Writing a test

```python
@test(id="M-NN", title="…", part="8 · UX", setup=s_none, needs_model=True, since="v0.5",
      runs=[Run(["push the login changes"], steps=[
          maybe_menu("Push only some changes", "Stage which files"),  # model may ask first
          Step("Stage which files", ENTER),
          Step(PLAN, ENTER)])],
      watch="What a human should judge on the screen.")
def c_mNN(fx, r):
    return [exit_is(r[0], 0), ok("only login files pushed", …), no_crash(r[0])]
```

- `Step(wait, keys)`: wait until `wait` is on screen (a tuple = any of them), then send
  `keys` — bytes, or `pick("label")` (the menu row's digit), `confirm_typed()` (type the
  word a type-to-confirm asks for), `plan_confirm()` (the plan's one confirmation: the
  typed value if it asks for one, else Enter), `if_menu("label")` (only if the model's
  "which did you mean?" menu is showing), `if_choice("label")` (only if any menu is waiting).
- Choose menu rows by label, never by position.
- Model-routed requests can legitimately get a "which did you mean?" menu — use
  `maybe_menu` so the test answers it instead of hanging.
- `Run(mode="pipe")` runs with no terminal; `model="down"` points at a dead port;
  `cwd="elsewhere"` runs outside any repository.
- Prefer checks on behaviour — exit code, repository state, which prompts appeared
  (`snap(r, label)` is the screen at a step; `plan_block`, `menu_rows` read it). A check on
  exact wording taken from a fix plan is marked `# copy: plan wording`, so it is easy to
  find and adjust when the implementation's final copy differs.
- To prove a new check bites, run it against the release that has the bug, into a scratch
  label (`suite/run.py auto scratch-041 M-NN`), and delete `runs/vscratch-041/` afterwards.
