#!/usr/bin/env python3
"""GiTrust acceptance suite (v0.4+): one definition per test, two ways to run it.

  auto    a pseudo-terminal (pyte) drives the release binary: it waits for text on
          the screen, presses the keys the test lists, then checks the exit code,
          the repository and the screen. Results go to runs/v<version>/results/<id>/.
  manual  the same setup, then the command runs live in YOUR terminal (recorded
          with `script`), you drive the prompts, and the same checks run after.

Every run is isolated: a scratch HOME (its own ~/.gitconfig, ~/.gitrust.toml and
~/.gitrust/trash), a throwaway bare remote and clone, kev_autostart off. Your real
config and ~/.gitrust are never touched. Tests that need the model expect a Kev
server on 127.0.0.1:8009 (see README: `kevctl.sh start`); model-down tests point at
a dead port instead.

Usage (from the repo root):
  uv run --with pyte python suite/run.py auto 0.5.0            # every test
  uv run --with pyte python suite/run.py auto 0.5.0 M-06 M-23  # some
  python3 suite/run.py manual 0.5.0 M-06                       # flagship, by hand
  python3 suite/run.py list                                    # ids, titles, flags
"""
import dataclasses, datetime, fcntl, json, os, pty, re, select, shutil, signal, struct
import subprocess, tempfile, termios, time
from typing import Callable, Optional

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
BIN = os.environ.get("GITRUST_BIN",
                     os.path.abspath(os.path.join(REPO_ROOT, "..", "Glit", "gitrust", "target",
                                                  "release", "gitrust")))
KEV_URL = os.environ.get("KEV_URL", "http://127.0.0.1:8009")
DEAD_URL = "http://127.0.0.1:9"          # nothing listens here: "the model is down"
REAL_UV_CACHE = os.environ.get("UV_CACHE_DIR", os.path.expanduser("~/.cache/uv"))
REAL_HF_HOME = os.environ.get("HF_HOME", os.path.expanduser("~/.cache/huggingface"))
COLS, ROWS = 110, 50

# Keys, as the terminal sends them.
ENTER, DOWN, UP, ESC, CTRL_C, SPACE = b"\r", b"\x1b[B", b"\x1b[A", b"\x1b", b"\x03", b" "
RIGHT, LEFT, BACKSPACE = b"\x1b[C", b"\x1b[D", b"\x7f"


def type_text(s: str) -> bytes:
    return s.encode()


def pick(label: str):
    """Keys that choose the menu row containing `label`: its digit in a numbered
    menu ("[2] …"), otherwise type-to-filter + Enter (inquire lists > 9 rows)."""
    import re

    def keys(screen: str) -> bytes:
        lines = screen.splitlines()
        for line in lines:
            if label in line:
                m = re.search(r"\[(\d)\]", line)
                if m:
                    return m.group(1).encode()
        # An arrow-key menu: rows follow the last "? " question line; ">" marks the cursor.
        q = max((i for i, l in enumerate(lines) if l.startswith("? ")), default=None)
        if q is not None:
            rows = []
            for l in lines[q + 1:]:
                if l.startswith("[") or not l.strip():
                    break
                rows.append(l)
            cur = next((i for i, l in enumerate(rows) if l.startswith(">")), 0)
            tgt = next((i for i, l in enumerate(rows) if label in l), None)
            if tgt is not None:
                d = tgt - cur
                return (DOWN * d if d > 0 else UP * -d) + ENTER
        return label.encode() + b"\r"
    return keys


def accept_prefilled():
    """Enter at a pre-filled text prompt (e.g. a quoted commit message to edit or
    accept); nothing if the plan is already showing."""
    def keys(screen: str) -> bytes:
        tail = screen.splitlines()[-2:] if screen else []
        return ENTER if any("Esc to cancel" in l for l in tail) else b""
    return keys


def if_menu(label: str):
    """Keys that pick `label` only if a "which did you mean?" menu is showing."""
    chooser = pick(label)

    def keys(screen: str) -> bytes:   # only the model's own question, not other menus
        return chooser(screen) if "which operation" in screen and "Esc cancel" in screen else b""
    return keys


TYPED_RE = re.compile(r"[Tt]ype '([^']+)'")     # a type-to-confirm prompt: "Type 'main' to …"


def confirm_typed():
    """Keys for a type-to-confirm prompt: type the word it asks for, then Enter."""
    def keys(screen: str) -> bytes:
        m = TYPED_RE.findall(screen)
        return (m[-1].encode() + b"\r") if m else b""
    return keys


def plan_confirm():
    """Keys for the plan's confirmation: the typed value when the plan asks for one
    in place of Enter (v0.5, D1), otherwise Enter. Only a prompt still waiting at the
    bottom of the screen counts — an answered one ("> …") is ignored."""
    def keys(screen: str) -> bytes:
        tail = [l for l in screen.splitlines() if l.strip()][-4:]
        m = TYPED_RE.findall("\n".join(l for l in tail if not l.startswith(">")))
        return (m[-1].encode() + b"\r") if m else ENTER
    return keys


def if_choice(label: str):
    """Keys that pick `label` if a menu is waiting (its key legend is the last line),
    otherwise nothing — for a menu that may or may not come before the plan."""
    chooser = pick(label)

    def keys(screen: str) -> bytes:
        last = screen.splitlines()[-1] if screen else ""
        return chooser(screen) if "Esc cancel" in last else b""
    return keys


# ---------------------------------------------------------------- reading screens
def snap(r, label: str) -> str:
    """The screen recorded at the step labelled `label` ("" if there was none)."""
    return next((s for l, s in r.snaps if l == label), "")


def logical_lines(screen: str) -> list:
    """Screen rows with the lines the terminal wrapped joined back into one."""
    out, cur = [], ""
    for row in screen.splitlines():
        cur += row
        if len(row) < COLS - 2:        # a full-width row continues on the next one
            out.append(cur)
            cur = ""
    if cur:
        out.append(cur)
    return out


def plan_block(screen: str) -> str:
    """The last plan on screen: from its "Plan · N steps" header to its key legend."""
    lines = screen.splitlines()
    start = max((i for i, l in enumerate(lines) if re.match(r"\s*Plan\b", l)), default=None)
    if start is None:
        return ""
    block = []
    for l in lines[start:]:
        block.append(l)
        if "[q] cancel" in l:
            break
    return "\n".join(block)


def menu_rows(screen: str) -> list:
    """The option rows of the last menu on screen (the rows under its "? question")."""
    lines = screen.splitlines()
    q = max((i for i, l in enumerate(lines) if l.startswith("? ")), default=None)
    if q is None:
        return []
    rows = []
    for l in lines[q + 1:]:
        if l.startswith("[") or not l.strip():
            break
        if l.startswith((">", "  ")):  # an option, not the rest of a wrapped question
            rows.append(l)
    return rows


# ---------------------------------------------------------------- data model
@dataclasses.dataclass
class Step:
    """Wait until `wait` is on screen (if given), then send `keys` (if given)."""
    wait: object = None                # text, or a tuple of texts (any of them)
    keys: object = None                # bytes, or fn(screen) -> bytes
    label: str = ""
    optional: bool = False             # not seeing `wait` is fine (e.g. the process ended)


@dataclasses.dataclass
class Run:
    argv: list                         # arguments after the binary
    steps: list = dataclasses.field(default_factory=list)
    mode: str = "pty"                  # "pty" (a terminal) or "pipe" (no terminal)
    stdin: str = ""                    # pipe mode only
    cwd: str = "work"                  # "work", "elsewhere" (not a repo)
    model: str = "up"                  # "up" (Kev on :8009) or "down" (dead port)
    timeout: int = 90
    note: str = ""                     # what to watch for (manual mode prints it)


@dataclasses.dataclass
class Test:
    id: str
    title: str
    part: str
    setup: Callable                    # (Fixture) -> None; builds the repo
    runs: list                         # [Run]
    check: Callable                    # (Fixture, [RunResult]) -> [(name, ok, detail)]
    needs_model: bool = False
    flagship: bool = False
    watch: str = ""                    # what a human should judge (manual mode, review)
    since: str = ""                    # "v0.2" for the original 31, "v0.4" for new ones


@dataclasses.dataclass
class RunResult:
    run: Run
    exit: Optional[int]
    screen: str                        # final screen (pty) or full output (pipe)
    snaps: list                        # [(label, screen)] in pty mode
    timed_out: list                    # wait texts that never appeared
    seconds: float


# ---------------------------------------------------------------- fixtures
def sh(cwd, *cmd, check=True, env=None):
    return subprocess.run(cmd, cwd=cwd, check=check, capture_output=True, text=True, env=env)


class Fixture:
    """A scratch world for one test: HOME, a bare remote, a clone in work/."""

    def __init__(self, test_id: str):
        self.root = tempfile.mkdtemp(prefix=f"gitrust-{test_id}-")
        self.home = os.path.join(self.root, "home")
        os.makedirs(self.home)
        with open(os.path.join(self.home, ".gitconfig"), "w") as f:
            f.write("[user]\n\tname = You\n\temail = you@example.invalid\n"
                    "[init]\n\tdefaultBranch = main\n[advice]\n\tdetachedHead = false\n")
        self.remote = os.path.join(self.root, "remote.git")
        self.work = os.path.join(self.root, "work")
        self.elsewhere = os.path.join(self.root, "not-a-repo")
        os.makedirs(self.elsewhere)
        self.vars = {}                 # anything a setup wants a check to see

    # --- environment for git and gitrust
    def env(self, model="up", debug=False):
        e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        e.update(HOME=self.home, UV_CACHE_DIR=REAL_UV_CACHE, HF_HOME=REAL_HF_HOME,
                 GIT_TERMINAL_PROMPT="0", TERM="xterm-256color", COLUMNS=str(COLS))
        e.pop("NO_COLOR", None)
        if debug:
            e["GITRUST_DEBUG"] = "1"
        url = KEV_URL if model == "up" else DEAD_URL
        with open(os.path.join(self.home, ".gitrust.toml"), "w") as f:
            f.write(f'kev_url = "{url}"\nkev_autostart = false\nkev_idle_minutes = 0\n')
        return e

    def git(self, *args, cwd=None, check=True):
        return sh(cwd or self.work, "git", *args, check=check, env=self.env()).stdout.strip()

    # --- builders
    def sandbox(self, remote=True):
        """main with one commit (app.txt = base), pushed to a bare remote."""
        if remote:
            sh(self.root, "git", "init", "-q", "--bare", "-b", "main", self.remote, env=self.env())
            sh(self.root, "git", "clone", "-q", self.remote, self.work, env=self.env())
        else:
            sh(self.root, "git", "init", "-q", "-b", "main", self.work, env=self.env())
        self.write("app.txt", "base\n")
        self.git("add", ".")
        self.git("commit", "-qm", "base")
        if remote:
            self.git("push", "-q", "-u", "origin", "main")
        return self

    def write(self, rel, text, append=False):
        p = os.path.join(self.work, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "a" if append else "w") as f:
            f.write(text)

    def read(self, rel):
        p = os.path.join(self.work, rel)
        return open(p).read() if os.path.exists(p) else None

    def commit(self, rel, text, msg, append=True):
        self.write(rel, text, append=append)
        self.git("add", rel)
        self.git("commit", "-qm", msg)
        return self.git("rev-parse", "HEAD")

    def teammate_pushes(self, rel="notes.txt", text="teammate hotfix\n", msg="teammate: hotfix",
                        branch="main"):
        mate = os.path.join(self.root, "teammate")
        if not os.path.exists(mate):
            sh(self.root, "git", "clone", "-q", self.remote, mate, env=self.env())
        sh(mate, "git", "checkout", "-q", branch, env=self.env())
        sh(mate, "git", "pull", "-q", env=self.env(), check=False)
        p = os.path.join(mate, rel)
        with open(p, "a") as f:
            f.write(text)
        sh(mate, "git", "add", rel, env=self.env())
        sh(mate, "git", "commit", "-qm", msg, env=self.env())
        sh(mate, "git", "push", "-q", "origin", branch, env=self.env())

    def head(self):
        return self.git("rev-parse", "HEAD")

    def contains(self, commit, rev="HEAD"):
        """True if `commit` is in the history of `rev`."""
        return sh(self.work, "git", "merge-base", "--is-ancestor", commit, rev, check=False,
                  env=self.env()).returncode == 0

    def branches(self):
        """Local branch names (a detached HEAD is not one)."""
        return self.git("for-each-ref", "--format=%(refname:short)", "refs/heads").split()

    def count(self, rev="HEAD"):
        return int(self.git("rev-list", "--count", rev))

    def ahead_behind(self):
        out = self.git("rev-list", "--left-right", "--count", "origin/main...HEAD", check=False)
        return tuple(int(x) for x in out.split()) if out else None

    def status(self):
        return self.git("status", "--porcelain")

    def trash_files(self):
        t = os.path.join(self.home, ".gitrust", "trash")
        out = []
        for dp, _, fs in os.walk(t):
            out += [os.path.relpath(os.path.join(dp, f), t) for f in fs]
        return sorted(out)

    def cleanup(self):
        t = os.path.join(self.home, ".gitrust", "trash")
        if os.path.isdir(t):
            os.chmod(t, 0o755)
        shutil.rmtree(self.root, ignore_errors=True)


# ---------------------------------------------------------------- the driver
def _screen_text(screen):
    lines = [l.rstrip() for l in screen.display]
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def drive_pty(argv, cwd, env, steps, timeout):
    """Run argv in a pseudo-terminal; returns (exit, final_screen, snaps, timed_out)."""
    import pyte

    class TtyScreen(pyte.Screen):
        fd = None

        def write_process_input(self, data):        # answer cursor-position queries
            if self.fd is not None:
                os.write(self.fd, data.encode())

    pid, fd = pty.fork()
    if pid == 0:                       # child: never fall back into the harness
        try:
            os.chdir(cwd)
            os.execvpe(argv[0], argv, env)
        finally:
            os._exit(127)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", ROWS, COLS, 0, 0))
    screen = TtyScreen(COLS, ROWS)
    screen.fd = fd
    stream = pyte.ByteStream(screen)
    snaps, timed_out = [], []
    deadline = time.time() + timeout
    state = {"exited": False, "status": None}

    def pump(t):
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.05)
            if r:
                try:
                    data = os.read(fd, 65536)
                except OSError:
                    data = b""
                if data:
                    stream.feed(data)
            if not state["exited"]:
                p, st = os.waitpid(pid, os.WNOHANG)
                if p:
                    state["exited"], state["status"] = True, st
                    try:
                        while True:
                            r, _, _ = select.select([fd], [], [], 0.1)
                            if not r:
                                break
                            data = os.read(fd, 65536)
                            if not data:
                                break
                            stream.feed(data)
                    except OSError:
                        pass
                    return

    def seen(w):
        txt = _screen_text(screen)
        return any(x in txt for x in w) if isinstance(w, tuple) else w in txt

    for st in steps:
        if st.wait:
            while time.time() < deadline and not seen(st.wait) and not state["exited"]:
                pump(0.2)
            if not seen(st.wait) and not st.optional:
                timed_out.append(st.wait)
        pump(0.5)
        snaps.append((st.label or (f"waited for {st.wait!r}" if st.wait else "step"),
                      _screen_text(screen)))
        if st.keys and not state["exited"]:
            keys = st.keys(_screen_text(screen)) if callable(st.keys) else st.keys
            if keys:
                os.write(fd, keys)
    while time.time() < deadline and not state["exited"]:
        pump(0.3)
    final = _screen_text(screen)
    if not state["exited"]:
        # Close the terminal BEFORE reaping: on macOS a killed process with unread
        # terminal output can't finish exiting while the master end is still open.
        os.kill(pid, signal.SIGKILL)
        os.close(fd)
        os.waitpid(pid, 0)
        timed_out.append("<process exit>")
        return None, final, snaps, timed_out
    code = os.waitstatus_to_exitcode(state["status"])
    os.close(fd)
    return code, final, snaps, timed_out


def execute(fx: Fixture, run: Run) -> RunResult:
    cwd = fx.work if run.cwd == "work" else fx.elsewhere
    env = fx.env(run.model)
    t0 = time.time()
    if run.mode == "pipe":
        p = subprocess.run([BIN, *run.argv], cwd=cwd, env=dict(env, NO_COLOR="1"),
                           input=run.stdin, capture_output=True, text=True, timeout=run.timeout)
        return RunResult(run, p.returncode, (p.stdout + p.stderr).rstrip(), [], [],
                         time.time() - t0)
    code, final, snaps, timed_out = drive_pty([BIN, *run.argv], cwd, env, run.steps, run.timeout)
    return RunResult(run, code, final, snaps, timed_out, time.time() - t0)


def execute_manual(fx: Fixture, run: Run, log_path: str) -> RunResult:
    """Run attached to the user's terminal, recorded with `script`."""
    cwd = fx.work if run.cwd == "work" else fx.elsewhere
    env = fx.env(run.model)
    t0 = time.time()
    if run.mode == "pipe":
        r = execute(fx, run)
        print(r.screen)
        return r
    p = subprocess.run(["script", "-q", log_path, BIN, *run.argv], cwd=cwd, env=env)
    raw = open(log_path, errors="replace").read() if os.path.exists(log_path) else ""
    return RunResult(run, p.returncode, _strip_ansi(raw), [], [], time.time() - t0)


def _strip_ansi(s):
    import re
    s = re.sub(r"\x1b\[[0-9;?]*[ -/]*[@-~]", "", s)
    s = re.sub(r"\x1b[()][0-9A-Za-z]", "", s)
    return s.replace("\r", "")


# ---------------------------------------------------------------- checks
def ok(name, cond, detail=""):
    return (name, bool(cond), detail)


def exit_is(r: RunResult, code, name=None):
    return ok(name or f"exits {code}", r.exit == code, f"exit={r.exit}")


def shows(r: RunResult, text, name=None):
    return ok(name or f"screen shows {text!r}", text in r.screen, "")


def lacks(r: RunResult, text, name=None):
    return ok(name or f"screen never shows {text!r}",
              text not in r.screen and all(text not in s for _, s in r.snaps), "")


def no_crash(r: RunResult):
    bad = [t for t in ("panicked", "RUST_BACKTRACE", "caused by:", "stack backtrace")
           if t in r.screen or any(t in s for _, s in r.snaps)]
    return ok("no panic / raw error chain", not bad and r.exit != 101, ", ".join(bad))


# ---------------------------------------------------------------- results
def kev_info():
    import urllib.request
    try:
        m = json.loads(urllib.request.urlopen(KEV_URL + "/v1/models", timeout=3).read())["models"][0]
        return {"run": m["run"], "temperature": m["temperature"], "backend": m.get("backend")}
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}


def binary_version():
    try:
        return subprocess.run([BIN, "--version"], capture_output=True, text=True).stdout.split()[-1]
    except Exception:  # noqa: BLE001
        return "?"


def suite_commit():
    """The commit of this repo the suite ran from ("+edits" if suite/ had uncommitted
    changes) — a run's expectations are the suite at that commit (README: Versions)."""
    try:
        sha = sh(REPO_ROOT, "git", "rev-parse", "--short", "HEAD").stdout.strip()
        dirty = sh(REPO_ROOT, "git", "status", "--porcelain", "--", "suite").stdout.strip()
        return sha + ("+edits" if dirty else "")
    except Exception:  # noqa: BLE001
        return "?"


def write_record(run_dir, test: Test, results, checks, mode, fx: Fixture):
    out = os.path.join(run_dir, "results", test.id)
    os.makedirs(out, exist_ok=True)
    passed = all(c[1] for c in checks)
    timeouts = [t for r in results for t in r.timed_out]
    verdict = "PASS" if passed and not timeouts else "FAIL"
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    rec = {"id": test.id, "title": test.title, "part": test.part, "mode": mode,
           "flagship": test.flagship, "needs_model": test.needs_model, "since": test.since,
           "auto_verdict": verdict, "when": now,
           "checks": [{"name": n, "ok": o, "detail": d} for n, o, d in checks],
           "runs": [{"argv": r.run.argv, "mode": r.run.mode, "model": r.run.model,
                     "exit": r.exit, "seconds": round(r.seconds, 1), "timed_out": r.timed_out}
                    for r in results],
           "vars": {k: str(v) for k, v in fx.vars.items()}}
    json.dump(rec, open(os.path.join(out, "result.json"), "w"), indent=1, ensure_ascii=False)
    with open(os.path.join(out, "screens.txt"), "w") as f:
        for i, r in enumerate(results, 1):
            f.write(f"######## run {i}: gitrust {' '.join(repr(a) for a in r.run.argv)}"
                    f"  [{r.run.mode}, model {r.run.model}]  exit={r.exit}  {r.seconds:.1f}s\n")
            for label, s in r.snaps:
                f.write(f"\n--- {label} ---\n{s}\n")
            f.write(f"\n--- final ---\n{r.screen}\n\n")
    review_path = os.path.join(out, "review.md")
    review = open(review_path).read() if os.path.exists(review_path) else ""
    lines = [f"# {test.id} · {test.title}", "",
             "| | |", "|---|---|",
             f"| **Part** | {test.part} |",
             f"| **Model** | {'yes' if test.needs_model else 'no'} |",
             f"| **Flagship** | {'★ yes' if test.flagship else 'no'} |",
             f"| **Run** | {mode} · {now} |",
             f"| **Automatic checks** | {'✅ all passed' if verdict == 'PASS' else '❌ failed'} |",
             "", "## Checks", ""]
    for n, o, d in checks:
        lines.append(f"- {'✅' if o else '❌'} {n}" + (f" — `{d}`" if d and not o else ""))
    if timeouts:
        lines.append(f"- ❌ waited for text that never appeared: {timeouts}")
    lines += ["", "## What a human should judge", "", test.watch or "—", "",
              "## Evidence", "", "- [`screens.txt`](screens.txt) — every screen, run by run",
              "- [`result.json`](result.json) — checks, exit codes, timings"]
    if review:
        lines += ["", "## Review", "", review.strip()]
    open(os.path.join(out, "README.md"), "w").write("\n".join(lines) + "\n")
    return verdict
