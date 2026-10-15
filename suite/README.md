# The v0.4 suite — how to run it

One Python definition per test ([`tests_v04.py`](tests_v04.py)), run two ways by
[`run.py`](run.py) on top of [`gitrust_suite.py`](gitrust_suite.py).

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
uv run --with pyte python suite/run.py auto 0.4.1                # everything (~15 min)
uv run --with pyte python suite/run.py auto 0.4.1 M-06 M-23      # some
uv run --with pyte python suite/run.py auto 0.4.1 --shard=0/4    # 1 of 4 parallel shards
python3 suite/run.py manual 0.4.1 M-06                           # a flagship, by hand
python3 suite/rollup.py 0.4.1                                    # rebuild runs/v0.4.1/README.md
python3 eval/run_eval.py 0.4.1                                   # the eval (see ../eval/)
```

In **manual** mode the runner prints what to watch for and which prompts to expect, waits
for Enter, then hands you the terminal. Answer the prompts as a user would (the expected
choice is in the test's `watch` line). The checks then run as usual and the recording is
saved next to the auto results. To record the screen for the README, start QuickTime /
`asciinema rec` before pressing Enter and drop the file in `runs/v<version>/evidence/`.

## Writing a test

```python
@test(id="M-43", title="…", part="8 · UX", setup=s_none, needs_model=True, since="v0.5",
      runs=[Run(["push the login changes"], steps=[
          maybe_menu("Push only some changes", "Stage which files"),  # model may ask first
          Step("Stage which files", ENTER),
          Step(PLAN, ENTER)])],
      watch="What a human should judge on the screen.")
def c_m43(fx, r):
    return [exit_is(r[0], 0), ok("only login files pushed", …), no_crash(r[0])]
```

- `Step(wait, keys)`: wait until `wait` is on screen (a tuple = any of them), then send
  `keys` — bytes, or `pick("label")` (the menu row's digit), `confirm_typed()` (type the
  word a type-to-confirm asks for), `if_menu("label")` (only if a menu is showing).
- Choose menu rows by label, never by position.
- Model-routed requests can legitimately get a "which did you mean?" menu — use
  `maybe_menu` so the test answers it instead of hanging.
- `Run(mode="pipe")` runs with no terminal; `model="down"` points at a dead port;
  `cwd="elsewhere"` runs outside any repository.
