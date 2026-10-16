"""The GiTrust acceptance suite as data (see gitrust_suite.py): the expectations of
v0.5.0. Older releases' expectations live in git history (suite/README.md, "Versions").

M-00…M-30 keep the ids and intent of the original 31-test suite (MANUAL_TEST_SUITE.md,
v0.2/v0.3), so results compare across versions; their expectations were updated for
v0.4 (Kev instead of Ollama, user-written commit messages, every cancel exits 1).
M-31…M-42 were new in v0.4: the UX conventions and the model's behaviour.
M-43 onwards are new in v0.5: the v0.4.1 findings (runs/v0.4.1/REPORT.md, F1–F20).

v0.5.0 follows GiTrust's docs/v0.5.0_fix_plan.md, decisions D1–D9 as accepted. What
changed for the suite: one confirmation, at the plan — where a typed value is needed it
replaces Enter (D1, D2); queries exit 0 when they ran, operations exit 1 when they didn't
happen (D4); git's own output only under a failed step (D6); no Cancel rows and no
dead-end menus (D7); a guard blocks before any plan renders.

Checks that match the fix plan's exact wording are marked `# copy: plan wording` —
adjust them if the implementation's final copy differs. Everything else checks
behaviour: exit codes, the repository, which prompts appeared.

Waiting on screen text: "[Enter] run" = the plan prompt; "Esc to cancel" = a text
prompt; "Esc cancel" = a menu; "Type '…'" = a typed confirmation. Menu options are
chosen by label (`pick`), never by position.
"""
import os
import re

from gitrust_suite import (BACKSPACE, CTRL_C, ENTER, ESC, TYPED_RE, Run, Step, Test, execute,
                           accept_prefilled, exit_is, if_choice, if_menu, lacks, logical_lines,
                           menu_rows, no_crash, ok, pick, plan_block, plan_confirm, shows, snap,
                           type_text)

PLAN = "[Enter] run"
TEXT = "Esc to cancel"
MENU = "Esc cancel"
CANCELED = "Canceled — nothing was done."
CONFIRM = ("Type '", "type '", PLAN)        # the plan's confirmation: a typed value, or Enter
AT_PLAN = "confirmation at the plan"
RAW_GIT = ("Successfully rebased", "Enumerating objects", "Removing ")   # F12: git's own output

TESTS = []


def maybe_menu(label, then):
    """The model may ask "which did you mean?" before `then` appears: if it does, pick
    `label` (asking is correct, safe behaviour — the screens record that it happened)."""
    then = then if isinstance(then, tuple) else (then,)
    return Step(("which operation",) + then, if_menu(label), "model: routed or asked",
                optional=True)


def maybe_prefilled():
    """A quoted commit message is offered pre-filled to edit or accept: accept it."""
    return Step((TEXT, PLAN), accept_prefilled(), "message (pre-filled)", optional=True)


def confirm_at_plan():
    """The plan's one confirmation: type the value if the plan asks for one, else Enter."""
    return Step(CONFIRM, plan_confirm(), AT_PLAN)


def v04_asks_again():
    """v0.4 asked for a type-to-confirm *before* the plan, then Enter at the plan (F9).
    Answering that second prompt lets an old binary finish (the one-confirmation checks
    still fail it); v0.5 never shows it, so the step is skipped."""
    return Step(PLAN, ENTER, "v0.4 flow: the plan asked again", optional=True)


def enter_or_v04_yes(screen):
    """Enter at the plan — or "y" if v0.4's separate (Y/n) question is waiting instead (F9),
    so an old binary can finish; the checks still fail it."""
    last = screen.splitlines()[-1] if screen else ""
    return b"y\r" if "(Y/n)" in last else ENTER


def one_confirmation(r, word=None):
    """D1: one confirmation, after the plan — the typed value is asked with the plan on
    screen above it, and nothing asks again after it. `word`: the value it must ask for."""
    s = snap(r, AT_PLAN).splitlines()
    typed = [i for i, l in enumerate(s) if TYPED_RE.search(l)]
    plans = [i for i, l in enumerate(s) if re.match(r"\s*Plan\b", l)]
    final = r.screen.splitlines()
    last = max((i for i, l in enumerate(final) if TYPED_RE.search(l)), default=None)
    out = [ok("typed confirmation asked at the plan (the plan is above it)",
              typed and plans and plans[-1] < typed[-1]),
           ok("nothing asks again after the typed value",
              last is not None and PLAN not in "\n".join(final[last + 1:]))]
    if word:
        asked = TYPED_RE.findall("\n".join(s))
        out.append(ok(f"the typed word is '{word}'", asked[-1:] == [word], str(asked[-1:])))
    return out


def no_raw_git(*results, extra=()):
    """F12 (D6): git's own output is hidden when a step succeeds."""
    return [lacks(x, t, f"no raw git output {t.strip()!r}" + (f" (run {i})" if len(results) > 1 else ""))
            for i, x in enumerate(results, 1) for t in RAW_GIT + tuple(extra)]


def says(r, text, name=None):
    """`text` is on the final screen, even if the terminal wrapped it across rows."""
    return ok(name or f"screen says {text!r}", any(text in l for l in logical_lines(r.screen)))


def rescue_menu(r, branch, plan_label):
    """F10 + F6: the detached-HEAD rescue is a numbered menu without a Cancel row, and the
    branch it makes is a step of the plan — nothing is created before the plan."""
    rows = menu_rows(snap(r, "rescue choice"))
    labels = [re.sub(r"^\s*>?\s*(\[\d\]\s*)?", "", x) for x in rows]
    plan = plan_block(snap(r, plan_label))
    return [ok("rescue menu is numbered", rows and all(re.match(r"\s*>?\s*\[\d\]", x) for x in rows),
               " | ".join(rows)),
            ok("rescue menu has no Cancel row", not any(l.startswith("Cancel") for l in labels),
               " | ".join(rows)),
            ok("rescue offers 'Create a branch here to keep this work'",
               "Create a branch here to keep this work" in snap(r, "rescue choice")),  # copy: plan wording
            ok(f"the plan shows the new branch {branch!r}", branch in plan, plan)]


def test(**kw):
    def deco(check):
        TESTS.append(Test(check=check, **kw))
        return check
    return deco


# ============================================================ Part 0 — setup
def s_none(fx):
    fx.sandbox()


@test(id="M-00", title="Binary version and help", part="0 · Setup", setup=s_none, since="v0.2",
      runs=[Run(["--version"], mode="pipe"), Run(["help"], mode="pipe")],
      watch="Version matches the run folder; `gitrust help` reads as a useful cheat-sheet.")
def c_m00(fx, r):
    return [exit_is(r[0], 0, "--version exits 0"), shows(r[0], "gitrust 0."),
            exit_is(r[1], 0, "help exits 0"), shows(r[1], "status"), no_crash(r[1])]


# ============================================================ Part 1 — everyday
@test(id="M-01", title="Exact phrase works with the model down", part="1 · Everyday",
      setup=s_none, since="v0.2",
      runs=[Run(["status"], model="down")],
      watch="Instant; ⚡ line; no complaint about the model.")
def c_m01(fx, r):
    return [exit_is(r[0], 0), shows(r[0], "Show status"), lacks(r[0], "isn't running"),
            shows(r[0], "Remote state as of", "status says how old the remote view is"),
            no_crash(r[0])]


@test(id="M-02", title="Model classification of a read-only request", part="1 · Everyday",
      setup=s_none, needs_model=True, since="v0.2",
      runs=[Run(["anything new in my repo?"], steps=[maybe_menu("Show history", "On branch")])],
      watch="✦ line names what was understood with a time; output is history or status.")
def c_m02(fx, r):
    s = r[0].screen
    return [exit_is(r[0], 0), ok("routed to history or status",
                                 "Show history" in s or "Show status" in s, s[:120]),
            lacks(r[0], "p=", "no model probability shown"), no_crash(r[0])]


def s_m03(fx):
    fx.sandbox()
    fx.write("app.txt", "change\n", append=True)


@test(id="M-03", title="Commit: the message is yours, [e] edits it", part="1 · Everyday",
      setup=s_m03, needs_model=True, since="v0.2",
      runs=[Run(["commit this"], steps=[
          maybe_menu("Commit everything", TEXT),
          Step(TEXT, type_text("first try") + ENTER, "message prompt"),
          Step(PLAN, b"e", "plan"),
          Step(TEXT, BACKSPACE * 12 + type_text("my message") + ENTER, "edit message"),
          Step(PLAN, ENTER, "plan again")])],
      watch="GiTrust asks for the message (never drafts one); the plan shows it; `e` edits it.")
def c_m03(fx, r):
    return [exit_is(r[0], 0), ok("commit subject is the edited text",
                                 fx.git("log", "-1", "--format=%s") == "my message",
                                 fx.git("log", "-1", "--format=%s")),
            ok("tree clean afterwards", fx.status() == "", fx.status()), no_crash(r[0])]


def s_m04(fx):
    fx.sandbox()
    fx.write("login.txt", "login page\n")
    fx.write("auth_login.txt", "login helper\n")
    fx.write("readme.txt", "unrelated notes\n")


@test(id="M-04", title="Scoped push: only the login files", part="1 · Everyday",
      setup=s_m04, needs_model=True, flagship=True, since="v0.2",
      runs=[Run(["push the login changes with message 'login page'"], steps=[
          maybe_menu("Push only some changes", "Stage which files"),
          Step("Stage which files", ENTER, "file picker"),
          maybe_prefilled(),
          Step(PLAN, ENTER, "plan")], timeout=150)],
      watch="The topic survives the quoted message (F5): the picker pre-selects the login files, "
            "shows +N −M and a reason per file; readme.txt not pre-selected; 'login page' is "
            "offered as the message; only login files reach the remote.")
def c_m04(fx, r):
    pushed = fx.git("show", "--name-only", "--format=", "origin/main", check=False).split()
    subject = fx.git("log", "-1", "--format=%s", "origin/main", check=False)
    return [exit_is(r[0], 0), ok("login.txt pushed", "login.txt" in pushed, str(pushed)),
            ok("readme.txt NOT pushed", "readme.txt" not in pushed, str(pushed)),
            ok("readme.txt still uncommitted", "readme.txt" in fx.status(), fx.status()),
            ok("the quoted message is the commit's subject", subject == "login page", subject),
            no_crash(r[0])]


def s_m05(fx):
    fx.sandbox()
    fx.git("checkout", "-qb", "other")
    fx.commit("app.txt", "other branch line\n", "other: app")
    fx.git("checkout", "-q", "main")
    fx.write("app.txt", "my uncommitted edit\n", append=True)   # switching would overwrite it


@test(id="M-05", title="Create a branch; dirty switch is handled", part="1 · Everyday",
      setup=s_m05, since="v0.2",
      runs=[Run(["create branch feature-x"], steps=[Step(PLAN, ENTER)]),
            Run(["switch to other"], steps=[Step(PLAN, ENTER, optional=True)], timeout=40),
            Run(["switch to main"], steps=[Step(PLAN, ENTER, optional=True)], timeout=40)],
      watch="Branch created. Switching with an edit the switch would overwrite is blocked before "
            "any plan, naming the file and the way out (commit or stash) — never a raw libgit2 "
            "error, never lost edits (F18). Switching to the branch you're on says so (F17).")
def c_m05(fx, r):
    edit_kept = "my uncommitted edit" in (fx.read("app.txt") or "")
    on = fx.git("branch", "--show-current")
    return [exit_is(r[0], 0, "branch created (exit 0)"),
            ok("feature-x exists", "feature-x" in fx.git("branch", "--list")),
            ok("the uncommitted edit survives the switch attempt", edit_kept),
            exit_is(r[1], 1, "the blocked switch exits 1"),
            lacks(r[1], PLAN, "the switch is blocked before any plan"),
            says(r[1], "would overwrite your uncommitted changes to app.txt"),  # copy: plan wording
            exit_is(r[2], 0, "switching to the current branch exits 0 (D4: the end state holds)"),
            says(r[2], "Already on main."),  # copy: plan wording
            ok("still on main", on == "main", on),
            no_crash(r[0]), no_crash(r[1]), no_crash(r[2])]


# ============================================================ Part 2 — divergence
def s_diverged(fx):
    fx.sandbox()
    fx.teammate_pushes()
    fx.commit("app.txt", "my feature\n", "feat: mine")
    fx.git("fetch", "-q")
    fx.vars["mine"] = fx.head()


@test(id="M-06", title="Diverged push → rebase → pushed", part="2 · Divergence",
      setup=s_diverged, flagship=True, since="v0.2",
      runs=[Run(["push"], steps=[Step(MENU, pick("ebase"), "reconcile choice"),
                                 Step(PLAN, ENTER, "plan")], timeout=90)],
      watch="The rebase/merge choice explains both in plain words, hints not cut off; rebase + "
            "push in one go; no 'pull first' warning on a plan that already rebases; no raw git "
            "output.")
def c_m06(fx, r):
    log = fx.git("log", "--format=%s")
    rows = menu_rows(snap(r[0], "reconcile choice"))
    return [exit_is(r[0], 0), ok("in sync with origin (0 0)", fx.ahead_behind() == (0, 0),
                                 str(fx.ahead_behind())),
            ok("teammate commit below mine", log.index("feat: mine") < log.index("teammate"), log),
            ok("linear history (no merge commit)",
               len(fx.git("log", "-1", "--format=%P").split()) == 1),
            ok("menu hints aren't cut off with '…' (F17)",
               rows and not any(x.endswith("…") for x in rows), " | ".join(rows)),
            lacks(r[0], "Consider pulling first", "no 'Consider pulling first' (F13)"),
            *no_raw_git(r[0]), no_crash(r[0])]


@test(id="M-07", title="Diverged push → merge", part="2 · Divergence", setup=s_diverged,
      since="v0.2",
      runs=[Run(["push"], steps=[Step(MENU, pick("erge"), "reconcile choice"),
                                 Step(PLAN, ENTER, "plan")], timeout=90)],
      watch="Merge path: a merge commit, then pushed; no 'pull first' warning.")
def c_m07(fx, r):
    return [exit_is(r[0], 0), ok("in sync with origin (0 0)", fx.ahead_behind() == (0, 0),
                                 str(fx.ahead_behind())),
            ok("merge commit has 2 parents",
               len(fx.git("log", "-1", "--format=%P").split()) == 2),
            lacks(r[0], "Consider pulling first", "no 'Consider pulling first' (F13)"),
            no_crash(r[0])]


def s_conflict(fx):
    fx.sandbox()
    fx.teammate_pushes(rel="app.txt", text="teammate line\n", msg="teammate: app")
    fx.commit("app.txt", "my line\n", "feat: my app change")
    fx.git("fetch", "-q")
    fx.vars["pre"] = fx.head()


@test(id="M-08", title="Rebase conflict → calm pause → continue", part="2 · Divergence",
      setup=s_conflict, since="v0.2",
      runs=[Run(["push"], steps=[Step(MENU, pick("ebase")), Step(PLAN, ENTER)], timeout=90)],
      watch="Pause message names the file, says nothing is lost, names continue/abort; exit ≠ 0. "
            "Continuing shows no 'interrupted pipeline' banner (the pause handed off, F7).")
def c_m08(fx, r):
    pause = [l for l in logical_lines(r[0].screen) if "nothing is lost" in l]
    checks = [ok("paused with a non-zero exit", r[0].exit not in (0, None), f"exit={r[0].exit}"),
              shows(r[0], "nothing is lost"), shows(r[0], "continue rebase"),
              ok("the pause names the conflicted file (F17)", any("app.txt" in l for l in pause),
                 " | ".join(pause)),
              ok("git is mid-rebase", os.path.isdir(os.path.join(fx.work, ".git", "rebase-merge"))
                 or os.path.isdir(os.path.join(fx.work, ".git", "rebase-apply"))), no_crash(r[0])]
    # Resolve and continue through gitrust (exact phrase, no model).
    fx.write("app.txt", "base\nteammate line\nmy line\n")
    fx.git("add", "app.txt")
    r2 = execute(fx, Run(["continue rebase"], steps=[Step(PLAN, ENTER)], timeout=60))
    r.append(r2)
    checks += [exit_is(r2, 0, "continue rebase exits 0"),
               ok("rebase finished", not os.path.isdir(os.path.join(fx.work, ".git",
                                                                    "rebase-merge"))),
               lacks(r2, "interrupted pipeline", "no 'interrupted pipeline' banner (F7)"),
               *no_raw_git(r[0], r2), no_crash(r2)]
    return checks


def s_conflict_paused(fx):
    s_conflict(fx)
    fx.git("rebase", "origin/main", check=False)


@test(id="M-09", title="Abort rebase restores exactly", part="2 · Divergence",
      setup=s_conflict_paused, since="v0.2",
      runs=[Run(["abort rebase"], steps=[Step(PLAN, ENTER)]), Run(["status"])],
      watch="Back to exactly where you were; status no longer talks about a rebase.")
def c_m09(fx, r):
    return [exit_is(r[0], 0), ok("HEAD back at the pre-rebase tip", fx.head() == fx.vars["pre"]),
            ok("status shows no rebase", "ebase in progress" not in r[1].screen), no_crash(r[0])]


def s_m10(fx):
    fx.sandbox()
    fx.git("remote", "set-head", "origin", "--auto")
    fx.git("checkout", "-qb", "feature")
    fx.commit("feature.txt", "feature work\n", "feat: feature")
    fx.teammate_pushes(rel="main.txt", text="main moved\n", msg="main: moved")
    fx.git("fetch", "-q")


@test(id="M-10", title="Sync feature with main", part="2 · Divergence", setup=s_m10,
      needs_model=True, since="v0.2",
      runs=[Run(["sync with main"], steps=[maybe_menu("Update from main", "ebase"),
                                           Step(MENU, pick("ebase")), Step(PLAN, ENTER)],
                timeout=90)],
      watch="Target resolves to main; rebase on an unpublished branch needs no force push; the "
            "closing note says how to push (not 're-run and confirm'); no raw git output.")
def c_m10(fx, r):
    return [exit_is(r[0], 0), ok("feature contains main's commit",
                                 fx.contains("origin/main") and
                                 "main: moved" in fx.git("log", "--format=%s")),
            lacks(r[0], "--force ", "no bare --force"),
            lacks(r[0], "re-run and confirm", "no 're-run and confirm' note (F17)"),
            *no_raw_git(r[0]), no_crash(r[0])]


# ============================================================ Part 3 — stuck states
@test(id="M-11", title="Mid-rebase commit request names the rebase", part="3 · Stuck states",
      setup=s_conflict_paused, needs_model=True, since="v0.2",
      runs=[Run(["commit my changes"], timeout=40)],
      watch="The answer is about the rebase (continue/abort), never 'checkout a branch'.")
def c_m11(fx, r):
    return [lacks(r[0], "checkout a branch"), shows(r[0], "rebase"),
            ok("did not exit 0 silently", r[0].exit != 0 or "rebase" in r[0].screen),
            no_crash(r[0])]


def s_m12(fx):
    fx.sandbox()
    fx.git("checkout", "-qb", "side")
    fx.commit("app.txt", "A\n", "side", append=False)
    fx.git("checkout", "-q", "main")
    fx.commit("app.txt", "B\n", "mainline", append=False)
    fx.git("merge", "side", check=False)
    fx.write("app.txt", "RESOLVED\n")
    fx.git("add", "app.txt")


@test(id="M-12", title="Commit a resolved merge: two parents", part="3 · Stuck states",
      setup=s_m12, needs_model=True, since="v0.2",
      runs=[Run(["commit the merge"], steps=[maybe_menu("Commit staged files", TEXT),
                                             Step(TEXT, ENTER, "message (MERGE_MSG offered)"),
                                             Step(PLAN, ENTER)], timeout=60)],
      watch="Git's merge message is offered; the commit has two parents.")
def c_m12(fx, r):
    return [exit_is(r[0], 0), ok("2 parents", len(fx.git("log", "-1", "--format=%P").split()) == 2),
            ok("merge finished", not os.path.exists(os.path.join(fx.work, ".git", "MERGE_HEAD"))),
            no_crash(r[0])]


def s_m13(fx):
    fx.sandbox()
    fx.git("checkout", "-q", fx.head())
    fx.write("app.txt", "x\n", append=True)


@test(id="M-13", title="Commit on a detached HEAD → rescue to a branch", part="3 · Stuck states",
      setup=s_m13, needs_model=True, since="v0.2",
      runs=[Run(["commit this with message 'detached work'"], steps=[
          maybe_menu("Commit everything", "ranch"),
          Step(MENU, pick("Create a branch"), "rescue choice"),
          Step(TEXT, BACKSPACE * 20 + type_text("rescued") + ENTER, "branch name"),
          maybe_prefilled(), Step(PLAN, ENTER, "plan")], timeout=60)],
      watch="Not a dead end: a numbered menu (no Cancel row) offers to make a branch here; the "
            "branch is the plan's first step, not done before it (F6, F10); the work ends up on it.")
def c_m13(fx, r):
    on = fx.git("symbolic-ref", "-q", "--short", "HEAD", check=False)
    return [ok("now on the new branch", on == "rescued", on),
            ok("the work is committed on it", fx.git("log", "-1", "--format=%s") == "detached work"
               and fx.status() == "", fx.status()),
            *rescue_menu(r[0], "rescued", "plan"), no_crash(r[0])]


def s_m14(fx):
    fx.sandbox()
    fx.git("checkout", "-q", fx.head())
    fx.vars["detached"] = fx.commit("app.txt", "y\n", "detached work")


@test(id="M-14", title="Switching away would strand a commit → guard", part="3 · Stuck states",
      setup=s_m14, flagship=False, since="v0.2",
      runs=[Run(["checkout main"], steps=[
          Step(MENU, pick("Create a branch"), "rescue choice"),
          Step(TEXT, BACKSPACE * 20 + type_text("saved-work") + ENTER, "branch name"),
          Step(PLAN, ENTER, "plan")], timeout=60)],
      watch="Says the commit would be stranded and offers a branch first (numbered menu, no Cancel "
            "row); the plan is: make the branch, then switch to main (F6, F10); nothing lost.")
def c_m14(fx, r):
    reach = fx.git("branch", "--contains", fx.vars["detached"], check=False)
    return [ok("the detached commit is on a branch", reach.strip() != "", reach),
            ok("saved-work holds the detached commit",
               fx.git("rev-parse", "saved-work", check=False) == fx.vars["detached"]),
            ok("on main afterwards (the request was 'checkout main')",
               fx.git("branch", "--show-current") == "main"),
            *rescue_menu(r[0], "saved-work", "plan"), no_crash(r[0])]


# ============================================================ Part 4 — undo family
def s_undo(fx):
    fx.sandbox()
    fx.vars["before"] = fx.head()
    fx.commit("app.txt", "v2\n", "feat: the mistake")


@test(id="M-15", title="Undo: four plain options, keep staged", part="4 · Undo",
      setup=s_undo, since="v0.2",
      runs=[Run(["undo"], steps=[Step(MENU, pick("keep the changes staged"), "undo choice"),
                                 Step(PLAN, ENTER)])],
      watch="Question names the commit; four options with consequences; numbered.")
def c_m15(fx, r):
    snap = r[0].snaps[0][1] if r[0].snaps else ""
    return [exit_is(r[0], 0), ok("names the commit", "feat: the mistake" in snap),
            ok("four options", all(x in snap for x in ("[1]", "[2]", "[3]", "[4]"))),
            ok("commit gone", fx.head() == fx.vars["before"]),
            ok("changes staged", fx.git("diff", "--cached", "--name-only") == "app.txt"),
            no_crash(r[0])]


def s_undo_dirty(fx):
    s_undo(fx)
    fx.write("app.txt", "uncommitted edit\n", append=True)


@test(id="M-16", title="Undo → throw away: type to confirm, trash backup", part="4 · Undo",
      setup=s_undo_dirty, flagship=True, since="v0.2",
      runs=[Run(["undo"], steps=[Step(MENU, pick("throw the changes away"), "undo choice"),
                                 confirm_at_plan(), v04_asks_again()], timeout=60)],
      watch="One confirmation (D1): the plan, its explanation, then the commit's SHA typed in "
            "place of Enter; the Risks text says uncommitted work is backed up, not gone; the "
            "success line names the backup.")
def c_m16(fx, r):
    return [exit_is(r[0], 0), ok("commit gone", fx.head() == fx.vars["before"]),
            ok("working tree clean", fx.status() == "", fx.status()),
            ok("trash backup written", any("app.txt" in t for t in fx.trash_files()),
               str(fx.trash_files())), shows(r[0], "backup"),
            *one_confirmation(r[0]),
            lacks(r[0], "is gone", "Risks doesn't say the uncommitted work 'is gone' (F17)"),
            no_crash(r[0])]


@test(id="M-17", title="--yes cannot undo", part="4 · Undo", setup=s_undo, since="v0.2",
      runs=[Run(["--yes", "undo"], mode="pipe")],
      watch="Refuses to choose for you, lists the choices, exit 1.")
def c_m17(fx, r):
    return [exit_is(r[0], 1), ok("HEAD untouched", fx.git("log", "-1", "--format=%s") ==
                                 "feat: the mistake"), shows(r[0], "Choices"), no_crash(r[0])]


def s_three(fx):
    fx.sandbox()
    for i in (1, 2, 3):
        fx.commit(f"f{i}.txt", f"{i}\n", f"commit {i}")
    fx.vars["tip"] = fx.head()
    fx.vars["tree"] = fx.git("rev-parse", "HEAD^{tree}")


@test(id="M-18", title="Undo 3 commits halts with guidance", part="4 · Undo", setup=s_three,
      needs_model=True, since="v0.2",
      runs=[Run(["undo the last 3 commits"], timeout=40)],
      watch="Guidance (squash / revert / undo one) before anything else — not an 'Undo the last "
            "commit' echo for a 3-commit request (F17); nothing changes.")
def c_m18(fx, r):
    return [exit_is(r[0], 1), ok("HEAD unchanged", fx.head() == fx.vars["tip"]),
            shows(r[0], "squash"),
            lacks(r[0], "Undo the last commit", "no 'Undo the last commit' echo (F17)"),
            no_crash(r[0])]


@test(id="M-19", title="Squash last 3: same content, one commit", part="4 · Undo",
      setup=s_three, needs_model=True, since="v0.2",
      runs=[Run(["squash the last 3 commits"], steps=[
          maybe_menu("Squash commits", TEXT),
          Step(TEXT, type_text("three in one") + ENTER, "message"),
          Step(PLAN, ENTER)], timeout=60)],
      watch="Asks for the squashed message with an empty prompt, the old subjects listed above "
            "it (D3); tree identical afterwards.")
def c_m19(fx, r):
    msg = fx.git("log", "-1", "--format=%B")
    return [exit_is(r[0], 0), ok("2 fewer commits", fx.count() == 2, str(fx.count())),
            ok("tree identical", fx.git("rev-parse", "HEAD^{tree}") == fx.vars["tree"]),
            ok("the message is exactly what was typed (D3: no pre-filled subjects)",
               msg == "three in one", repr(msg)),
            no_crash(r[0])]


def s_m20(fx):
    fx.sandbox()
    fx.commit("app.txt", "v2\n", "typo mesage")
    fx.git("push", "-q")


@test(id="M-20", title="Fix a pushed commit's message: escalate + lease", part="4 · Undo",
      setup=s_m20, needs_model=True, flagship=False, since="v0.2",
      runs=[Run(["fix the last commit message to 'typo message fixed'"], steps=[
          maybe_menu("Amend the last commit", CONFIRM),
          confirm_at_plan(), v04_asks_again()], timeout=90)],
      watch="Explains a force push is needed; one confirmation — the branch name typed at the "
            "plan (D1); uses --force-with-lease; no raw git output.")
def c_m20(fx, r):
    return [exit_is(r[0], 0), ok("message fixed on the remote",
                                 fx.git("log", "-1", "--format=%s", "origin/main") ==
                                 "typo message fixed"),
            ok("remote == local", fx.git("rev-parse", "origin/main") == fx.head()),
            lacks(r[0], "--force "), *one_confirmation(r[0]), *no_raw_git(r[0]),
            no_crash(r[0])]


# ============================================================ Part 5 — hooks
def s_hook(fx):
    fx.sandbox()
    hook = os.path.join(fx.work, ".git", "hooks", "pre-commit")
    open(hook, "w").write("#!/bin/sh\necho 'LINT FAILED'\nexit 1\n")
    os.chmod(hook, 0o755)
    fx.write("app.txt", "x\n", append=True)
    fx.vars["count"] = fx.count()


@test(id="M-21", title="A failing pre-commit hook blocks the commit", part="5 · Hooks",
      setup=s_hook, needs_model=True, since="v0.2",
      runs=[Run(["commit everything with message 'try it'"], steps=[
          maybe_menu("Commit everything", (TEXT, PLAN)), maybe_prefilled(), Step(PLAN, ENTER),
          Step("Pick one", ESC, "v0.4 flow: a menu after the hook failed", optional=True)],
                timeout=60)],
      watch="Says hooks were detected; the hook's output is shown once; then a plain message — "
            "no menu (D7): the files are still staged, fix what the hook reported and commit "
            "again; nothing committed; exit 1; never 'nothing was done'; no snapshot/--recover "
            "lines for a failure that only staged files.")
def c_m21(fx, r):
    return [exit_is(r[0], 1), shows(r[0], "LINT FAILED"),
            ok("the hook's output is shown once", r[0].screen.count("LINT FAILED") == 1,
               f"{r[0].screen.count('LINT FAILED')} times"),
            ok("no new commit", fx.count() == fx.vars["count"]),
            ok("the files are still staged", fx.git("diff", "--cached", "--name-only") == "app.txt"),
            lacks(r[0], "Pick one", "no menu after the failure (F8)"),
            says(r[0], "still staged", "the screen says the files are still staged"),  # copy: plan wording
            lacks(r[0], CANCELED, "never says 'nothing was done' (the files were staged)"),
            lacks(r[0], "--recover", "no snapshot / --recover advice when only staging ran (F8)"),
            no_crash(r[0])]


def s_m22(fx):
    s_hook(fx)
    fx.git("checkout", "--", "app.txt")
    fx.commit("other.txt", "o\n", "to be reverted")   # git commit runs the hook → bypass
    fx.vars["count"] = fx.count()


def s_m22_safe(fx):
    fx.sandbox()
    fx.commit("other.txt", "o\n", "to be reverted")
    hook = os.path.join(fx.work, ".git", "hooks", "pre-commit")
    open(hook, "w").write("#!/bin/sh\necho 'LINT FAILED'\nexit 1\n")
    os.chmod(hook, 0o755)
    fx.vars["count"] = fx.count()


@test(id="M-22", title="Revert succeeds despite the same hook", part="5 · Hooks",
      setup=s_m22_safe, since="v0.2",
      runs=[Run(["revert last commit"], steps=[
          Step((PLAN, "(Y/n)"), enter_or_v04_yes, "plan"),
          Step(PLAN, ENTER, "v0.4 flow: the plan after revert's own (Y/n)", optional=True)],
                timeout=60)],
      watch="Matches git: revert doesn't run pre-commit, so it succeeds. One confirmation — the "
            "plan, which names the commit by its subject, not just its SHA (D1, F17); no raw git "
            "output.")
def c_m22(fx, r):
    return [exit_is(r[0], 0), ok("one new (revert) commit", fx.count() == fx.vars["count"] + 1),
            ok("other.txt gone", fx.read("other.txt") is None),
            lacks(r[0], "(Y/n)", "no separate (Y/n) question — just the plan (F9)"),
            ok("the plan names the commit's subject", "to be reverted" in snap(r[0], "plan")),
            *no_raw_git(r[0], extra=("delete mode",)), no_crash(r[0])]


# ============================================================ Part 6 — forensics & trash
def s_m23(fx):
    fx.sandbox()
    fx.git("checkout", "-qb", "experiment")
    fx.vars["lost"] = fx.commit("precious.txt", "precious work\n", "the work I'll lose")
    fx.git("checkout", "-q", "main")
    fx.git("branch", "-D", "experiment")
    fx.vars["head"] = fx.head()


@test(id="M-23", title="Deleted branch → find my lost work", part="6 · Forensics",
      setup=s_m23, flagship=True, since="v0.2",
      runs=[Run(["find my lost work"], steps=[Step("the work I'll lose", pick("the work I'll lose"),
                                                   "browser")], timeout=60)],
      watch="Lists the lost commit in plain words; restores it to a rescue branch; your "
            "current branch and files untouched.")
def c_m23(fx, r):
    rescue = [b.strip(" *") for b in fx.git("branch", "--list", "rescue/*").splitlines()]
    at = fx.git("rev-parse", rescue[0]) if rescue else ""
    return [exit_is(r[0], 0), ok("a rescue branch exists", bool(rescue), str(rescue)),
            ok("rescue branch at the lost commit", at == fx.vars["lost"]),
            ok("HEAD untouched", fx.head() == fx.vars["head"]), no_crash(r[0])]


def s_m24(fx):
    fx.sandbox()
    fx.write("app.txt", "wip\n", append=True)
    fx.git("stash", "push", "-q", "-m", "important wip")
    fx.git("stash", "drop", "-q")


@test(id="M-24", title="A dropped stash surfaces", part="6 · Forensics", setup=s_m24,
      since="v0.2",
      runs=[Run(["find my lost work"], steps=[Step("important wip", pick("important wip"))],
                timeout=60)],
      watch="The dropped stash is listed — without git's internal 'index on …' commit beside it "
            "(F17) — and can be restored to a branch.")
def c_m24(fx, r):
    rescue = [b.strip(" *") for b in fx.git("branch", "--list", "rescue/*").splitlines()]
    has = rescue and "wip" in fx.git("show", f"{rescue[0]}:app.txt", check=False)
    return [exit_is(r[0], 0), ok("rescue branch has the wip change", bool(has), str(rescue)),
            lacks(r[0], "index on", "no internal 'index on …' row (F17)"), no_crash(r[0])]


@test(id="M-25", title="Nothing lost: an honest empty result", part="6 · Forensics",
      setup=s_none, since="v0.2", runs=[Run(["find my lost work"], timeout=40)],
      watch="Says nothing was found and why some work can't be recovered; exit 0 — a query that "
            "ran (D4).")
def c_m25(fx, r):
    return [exit_is(r[0], 0, "exits 0 (D4: a query that ran)"),
            shows(r[0], "may be unrecoverable"), no_crash(r[0])]


def s_m26(fx):
    fx.sandbox()
    fx.write("app.txt", "mod\n", append=True)
    fx.write("junk/inner/file.txt", "tmp\n")


@test(id="M-26", title="Clean up: counts, untracked deleted, backed up", part="6 · Forensics",
      setup=s_m26, since="v0.2",
      runs=[Run(["clean up my repo"], steps=[Step(MENU, pick("untracked"), "clean-up choice"),
                                             confirm_at_plan()], timeout=60)],
      watch="Gate shows how many files of each kind and names the backup. Deleting untracked "
            "files needs a typed word at the plan, like a hard reset (D2) — the backup is their "
            "only copy; the success line calls them deleted files, not discarded changes.")
def c_m26(fx, r):
    return [exit_is(r[0], 0), ok("junk/ deleted", not os.path.exists(os.path.join(fx.work, "junk"))),
            ok("backup holds junk/inner/file.txt",
               any(t.endswith("junk/inner/file.txt") for t in fx.trash_files()),
               str(fx.trash_files())),
            ok("tracked edit untouched", "mod" in (fx.read("app.txt") or "")),
            *one_confirmation(r[0], word="delete"),  # copy: plan wording
            lacks(r[0], "discarded changes", "the backup line doesn't call them 'discarded changes' (F17)"),
            *no_raw_git(r[0]), no_crash(r[0])]


def s_m27(fx):
    fx.sandbox()
    fx.write("keep-me.txt", "untracked\n")
    t = os.path.join(fx.home, ".gitrust", "trash")
    os.makedirs(t)
    os.chmod(t, 0)


@test(id="M-27", title="Backup can't be written → nothing deleted", part="6 · Forensics",
      setup=s_m27, since="v0.2",
      runs=[Run(["clean up my repo"], steps=[Step(MENU, pick("untracked"), "clean-up choice"),
                                             confirm_at_plan()], timeout=60)],
      watch="After the typed word, refuses in one plain line, once: the backup couldn't be "
            "written, so nothing was deleted, and how to fix it (a ~ path, no error chain, F2); "
            "the file still exists.")
def c_m27(fx, r):
    msg = "Couldn't back up your files first, so nothing was deleted."  # copy: plan wording
    flat = "".join(r[0].screen.splitlines()) + "".join("".join(s.splitlines()) for _, s in r[0].snaps)
    return [exit_is(r[0], 1),
            ok("untracked file still there", fx.read("keep-me.txt") is not None),
            *one_confirmation(r[0], word="delete"),  # copy: plan wording
            says(r[0], msg),
            ok("…said once", sum(l.count(msg) for l in logical_lines(r[0].screen)) == 1),
            ok("no absolute temp path on screen (the plan: a ~ path)", fx.home not in flat),
            no_crash(r[0])]


@test(id="M-28", title="--recover with nothing to recover points to forensics",
      part="6 · Forensics", setup=s_none, since="v0.2", runs=[Run(["--recover"], mode="pipe")],
      watch="Says there's nothing interrupted and suggests 'find my lost work'; exit 1 — an "
            "operation that didn't happen (D4).")
def c_m28(fx, r):
    return [exit_is(r[0], 1, "exits 1 (D4: nothing was recovered)"),
            shows(r[0], "find my lost work"), no_crash(r[0])]


# ============================================================ Part 7 — meta
@test(id="M-29", title="Model down: warning, full menu, refusals", part="7 · Meta",
      setup=s_none, since="v0.2",
      runs=[Run(["what changed in the auth files?"], model="down",
                steps=[Step(MENU, ESC, "manual menu")]),
            Run(["--yes", "what changed in the auth files?"], model="down", mode="pipe"),
            Run(["what changed"], model="down", mode="pipe", stdin="q\n"),
            Run(["status"], model="down")],
      watch="Warning names the fix; a menu of operations by title; --yes refuses with its own "
            "plain message for a model that's down (F15), no-terminal without suggesting --yes "
            "(F17) — both exit 1; status still instant.")
def c_m29(fx, r):
    return [shows(r[0], "isn't running"), ok("menu lists operations by title",
                                             "Show status" in (r[0].snaps[0][1] if r[0].snaps else "")),
            exit_is(r[0], 1, "Esc at the menu exits 1"), shows(r[0], CANCELED),
            exit_is(r[1], 1, "--yes refuses (exit 1)"),
            lacks(r[1], "type to filter", "--yes refusal doesn't paste the menu prompt (F15)"),
            says(r[1], "can't tell which operation you mean"),  # copy: plan wording
            exit_is(r[2], 1, "no terminal → exit 1"), shows(r[2], "no terminal to ask in"),
            lacks(r[2], "add --yes", "no-terminal advice for a menu doesn't suggest --yes (F17)"),
            exit_is(r[3], 0, "status still works"), no_crash(r[0]), no_crash(r[1]),
            no_crash(r[2])]


@test(id="M-30", title="Not a repository", part="7 · Meta", setup=s_none, since="v0.2",
      runs=[Run(["status"], cwd="elsewhere", mode="pipe")],
      watch="Friendly not-a-repo message, exit ≠ 0.")
def c_m30(fx, r):
    return [ok("non-zero exit", r[0].exit not in (0, None), f"exit={r[0].exit}"),
            no_crash(r[0])]


# ============================================================ Part 8 — v0.4: the UX conventions
@test(id="M-31", title="Esc at a menu: calm cancel, exit 1, nothing done", part="8 · UX",
      setup=s_undo, since="v0.4",
      runs=[Run(["undo"], steps=[Step(MENU, ESC)])],
      watch="One calm line, no error styling.")
def c_m31(fx, r):
    return [exit_is(r[0], 1), shows(r[0], CANCELED),
            ok("HEAD untouched", fx.git("log", "-1", "--format=%s") == "feat: the mistake"),
            no_crash(r[0])]


@test(id="M-32", title="q at the plan cancels; stray keys are ignored", part="8 · UX",
      setup=s_m03, since="v0.4",
      runs=[Run(["commit everything with message 'not this time'"],
                steps=[maybe_menu("Commit everything", (TEXT, PLAN)), maybe_prefilled(),
                       Step(PLAN, b"x", "stray key"), Step(PLAN, b"q", "q")])],
      watch="A stray key does nothing; q cancels; exit 1.")
def c_m32(fx, r):
    return [exit_is(r[0], 1), shows(r[0], "Canceled"),
            ok("nothing committed", fx.git("log", "-1", "--format=%s") == "base"), no_crash(r[0])]


@test(id="M-33", title="[s] at the plan: commit stays local", part="8 · UX", setup=s_m03,
      since="v0.4",
      runs=[Run(["commit and push"], steps=[Step(TEXT, type_text("local only") + ENTER),
                                            Step(PLAN, b"s", "skip push"),
                                            Step(PLAN, ENTER, "plan without push")], timeout=60)],
      watch="The legend offers [s] only because the plan pushes; after s the push step is gone.")
def c_m33(fx, r):
    return [exit_is(r[0], 0), ok("committed", fx.git("log", "-1", "--format=%s") == "local only"),
            ok("not pushed (ahead 1)", fx.ahead_behind() == (0, 1), str(fx.ahead_behind())),
            no_crash(r[0])]


@test(id="M-34", title="Numbered menu: a digit chooses at once", part="8 · UX", setup=s_undo,
      since="v0.4",
      runs=[Run(["undo"], steps=[Step(MENU, b"9", "invalid digit ignored"),
                                 Step(MENU, pick("keep the changes in my files"), "digit"),
                                 Step(PLAN, ENTER)])],
      watch="9 (no such row) is ignored; the right digit picks immediately.")
def c_m34(fx, r):
    return [exit_is(r[0], 0), ok("commit gone", fx.head() == fx.vars["before"]),
            ok("changes unstaged in files", fx.git("diff", "--name-only") == "app.txt"),
            no_crash(r[0])]


@test(id="M-35", title="Learned phrase: a menu pick is instant next time", part="8 · UX",
      setup=s_none, needs_model=True, since="v0.4",
      runs=[Run(["whats goin on"], steps=[Step(MENU, pick("Show status"), "which did you mean")],
                timeout=60),
            Run(["whats goin on"], model="down"),
            Run(["aliases"], mode="pipe"),
            Run(["aliases", "--forget", "whats goin on"], mode="pipe")],
      watch="Second run says '· learned' and works with the model down; `aliases` lists it.")
def c_m35(fx, r):
    return [exit_is(r[0], 0), shows(r[1], "learned"), exit_is(r[1], 0, "learned run exits 0"),
            shows(r[2], "whats goin on"), exit_is(r[3], 0, "forget exits 0"), no_crash(r[1])]


@test(id="M-36", title="Not a Git request: refused, exit 1", part="8 · UX", setup=s_none,
      needs_model=True, since="v0.4",
      runs=[Run(["write a python function that parses dates"], timeout=40)],
      watch="A polite refusal pointing at `gitrust help`.")
def c_m36(fx, r):
    return [exit_is(r[0], 1), shows(r[0], "doesn't look like a Git request"), no_crash(r[0])]


@test(id="M-37", title="Commit and push in one request", part="8 · UX", setup=s_m03,
      needs_model=True, since="v0.4",
      runs=[Run(["commit n push"], steps=[maybe_menu("Commit and push everything", TEXT),
                                          Step(TEXT, type_text("both at once") + ENTER),
                                          Step(PLAN, ENTER)], timeout=60)],
      watch="✦ Commit and push everything; asks for the message; pushed.")
def c_m37(fx, r):
    return [exit_is(r[0], 0), shows(r[0], "Commit and push"),
            ok("pushed (0 0)", fx.ahead_behind() == (0, 0), str(fx.ahead_behind())),
            ok("subject", fx.git("log", "-1", "--format=%s") == "both at once"), no_crash(r[0])]


@test(id="M-38", title="No terminal, a question needed: plain message, exit 1", part="8 · UX",
      setup=s_undo, since="v0.4", runs=[Run(["undo"], mode="pipe", stdin="")],
      watch="One readable line, no 'caused by'; it's a choice, so the advice is to run it in a "
            "terminal — not --yes, which never chooses (F17).")
def c_m38(fx, r):
    return [exit_is(r[0], 1), shows(r[0], "no terminal to ask in"),
            lacks(r[0], "add --yes", "the advice for a choice doesn't suggest --yes (F17)"),
            no_crash(r[0])]


def s_midrebase_status(fx):
    s_conflict_paused(fx)


@test(id="M-39", title="Status mid-rebase says what to do", part="8 · UX",
      setup=s_midrebase_status, since="v0.4", runs=[Run(["status"])],
      watch="Names the rebase, the conflicted file, and the continue/abort phrases.")
def c_m39(fx, r):
    return [shows(r[0], "Rebase in progress"), shows(r[0], "app.txt"),
            shows(r[0], "continue rebase"), no_crash(r[0])]


@test(id="M-40", title="Clean tree: 'commit everything' stops before asking", part="8 · UX",
      setup=s_none, since="v0.4", runs=[Run(["commit everything"], mode="pipe")],
      watch="Says nothing to commit before any message prompt.")
def c_m40(fx, r):
    return [shows(r[0], "Nothing to commit"), lacks(r[0], "message"), no_crash(r[0])]


@test(id="M-41", title="Output piped into head doesn't crash", part="8 · UX", setup=s_three,
      since="v0.4", runs=[Run(["--yes", "log"], mode="pipe")],
      watch="(checked by the runner with a closed pipe — see check). 'log' is an exact phrase, so "
            "no model is involved. v0.4.1's check (`… | head -1`) was a race: it caught the "
            "panic only when the reader left before the writes, so the reader now leaves first.")
def c_m41(fx, r):
    import subprocess
    from gitrust_suite import BIN
    # What `gitrust … | head -1` does when head exits early, made deterministic: the
    # pipe's reader is gone before the first write.
    rfd, wfd = os.pipe()
    os.close(rfd)
    try:
        c = subprocess.run([BIN, "--yes", "log"], cwd=fx.work, env=fx.env(), stdout=wfd,
                           stderr=subprocess.PIPE, text=True, timeout=60)
    finally:
        os.close(wfd)
    return [ok("no panic when the reader closes early", "panicked" not in c.stderr
               and c.returncode != 101, f"exit={c.returncode} stderr={c.stderr.strip()[:120]}"),
            ok("…and it runs to completion: exit 0 (D5)", c.returncode == 0, f"exit={c.returncode}")]


@test(id="M-42", title="Help lists only phrases that work instantly", part="8 · UX",
      setup=s_none, since="v0.4",
      runs=[Run(["help"], mode="pipe")] + [Run([p], model="down", mode="pipe")
                                           for p in ("log", "branches", "current branch",
                                                     "remotes", "config", "diff")],
      watch="Look-section phrases from help all work with the model down.")
def c_m42(fx, r):
    out = [exit_is(r[0], 0)]
    for x in r[1:]:
        out += [ok(f"'{x.run.argv[0]}' works with the model down",
                   x.exit == 0 and "isn't running" not in x.screen, f"exit={x.exit}")]
    return out


# ============================================================ v0.5: the v0.4.1 findings
def s_m43(fx):
    """develop and feature both branch from base; main moves on without either."""
    fx.sandbox()
    fx.git("remote", "set-head", "origin", "--auto")
    fx.git("checkout", "-qb", "develop")
    fx.vars["develop"] = fx.commit("develop.txt", "develop work\n", "develop: work")
    fx.git("push", "-q", "-u", "origin", "develop")
    fx.git("checkout", "-q", "main")
    fx.git("checkout", "-qb", "feature")
    fx.commit("feature.txt", "feature work\n", "feat: feature")
    fx.teammate_pushes(rel="main.txt", text="main moved\n", msg="main: moved")
    fx.git("fetch", "-q")
    fx.vars["main"] = fx.git("rev-parse", "origin/main")


@test(id="M-43", title="'merge develop into feature' brings in develop, not main",
      part="2 · Divergence", setup=s_m43, since="v0.5",
      runs=[Run(["merge develop into feature"], steps=[
          Step((MENU, PLAN), if_choice("Merge"), "rebase or merge?"),
          Step(PLAN, ENTER, "plan")], timeout=90)],
      watch="⚡ the echo names the real source ('Update from develop'); the plan merges develop — "
            "never main (F19); feature ends with develop's commit and without main's.")
def c_m43(fx, r):
    on = fx.git("branch", "--show-current")
    return [exit_is(r[0], 0), ok("still on feature", on == "feature", on),
            ok("feature contains develop's commit", fx.contains(fx.vars["develop"])),
            ok("feature does NOT contain main's new commit", not fx.contains(fx.vars["main"])),
            says(r[0], "Update from develop"),  # copy: plan wording
            no_crash(r[0])]


def s_m44(fx):
    """On feature, tracking origin/feature: a teammate pushed to feature, and main moved too."""
    fx.sandbox()
    fx.git("remote", "set-head", "origin", "--auto")
    fx.git("checkout", "-qb", "feature")
    fx.git("push", "-q", "-u", "origin", "feature")
    fx.teammate_pushes(rel="feature.txt", text="teammate on feature\n",
                       msg="teammate: feature work", branch="feature")
    fx.teammate_pushes(rel="main.txt", text="main moved\n", msg="main: moved")
    fx.git("fetch", "-q")
    fx.vars["theirs"] = fx.git("rev-parse", "origin/feature")
    fx.vars["main"] = fx.git("rev-parse", "origin/main")


@test(id="M-44", title="'Pull the latest from origin into this branch' is a pull",
      part="2 · Divergence", setup=s_m44, needs_model=True, since="v0.5",
      runs=[Run(["pull the latest from origin into this branch"], steps=[
          maybe_menu("Pull", PLAN), Step(PLAN, ENTER, "plan")], timeout=90)],
      watch="A pull of this branch from its own remote (✦ Pull, or a 'which did you mean?' menu) "
            "— never ⚡ 'Update from main' (F3): feature gets origin/feature's new commit, not "
            "main's.")
def c_m44(fx, r):
    on = fx.git("branch", "--show-current")
    echo = [l for x in [r[0].screen] + [s for _, s in r[0].snaps] for l in x.splitlines()
            if re.match(r"[⚡✦◇*+]\s+Update from main", l)]
    return [exit_is(r[0], 0), ok("still on feature", on == "feature", on),
            ok("feature has origin/feature's new commit", fx.contains(fx.vars["theirs"])),
            ok("feature does NOT contain main's new commit", not fx.contains(fx.vars["main"])),
            ok("not routed to 'Update from main'", not echo, " | ".join(echo[:1])),
            no_crash(r[0])]


@test(id="M-45", title="Rebase finished with plain git: no stale banner, --recover undoes nothing",
      part="2 · Divergence", setup=s_conflict, since="v0.5",
      runs=[Run(["push"], steps=[Step(MENU, pick("ebase"), "reconcile choice"),
                                 Step(PLAN, ENTER, "plan")], timeout=90)],
      watch="After the conflict pause the user finishes with plain `git rebase --continue`. The "
            "next command shows no 'interrupted pipeline' banner, and `--recover` says there's "
            "nothing to restore (exit 1) instead of resetting the branch to before the rebase (F7).")
def c_m45(fx, r):
    checks = [ok("paused on the conflict (exit ≠ 0)", r[0].exit not in (0, None), f"exit={r[0].exit}"),
              ok("git is mid-rebase", os.path.isdir(os.path.join(fx.work, ".git", "rebase-merge"))
                 or os.path.isdir(os.path.join(fx.work, ".git", "rebase-apply")))]
    # Resolve and finish with plain git, not gitrust.
    resolved = "base\nteammate line\nmy line\n"
    fx.write("app.txt", resolved)
    fx.git("add", "app.txt")
    fx.git("-c", "core.editor=true", "rebase", "--continue")
    done = fx.head()
    checks.append(ok("git finished the rebase (on top of the teammate's commit)",
                     fx.contains("origin/main")
                     and not os.path.isdir(os.path.join(fx.work, ".git", "rebase-merge"))))
    r2 = execute(fx, Run(["status"], timeout=40))
    r3 = execute(fx, Run(["--recover"], mode="pipe", timeout=40))
    r += [r2, r3]
    return checks + [
        exit_is(r2, 0, "status exits 0"),
        lacks(r2, "interrupted pipeline", "status shows no 'interrupted pipeline' banner"),
        lacks(r2, "--recover", "status doesn't send you to --recover"),
        exit_is(r3, 1, "--recover exits 1 (nothing to restore, D4)"),
        ok("--recover left HEAD where git's rebase put it", fx.head() == done,
           f"{fx.head()[:7]} vs {done[:7]}"),
        ok("the resolution is kept", fx.read("app.txt") == resolved and fx.status() == "",
           fx.status()),
        no_crash(r2), no_crash(r3)]


def s_m46(fx):
    s_m13(fx)                       # a detached HEAD with an uncommitted edit
    fx.vars["head"] = fx.head()
    fx.vars["branches"] = fx.branches()
    fx.vars["status"] = fx.status()


@test(id="M-46", title="Detached-HEAD rescue: q at the plan changes nothing",
      part="3 · Stuck states", setup=s_m46, since="v0.5",
      runs=[Run(["commit everything"], steps=[
          Step(MENU, pick("Create a branch"), "rescue choice"),
          Step(TEXT, BACKSPACE * 20 + type_text("kept-work") + ENTER, "branch name"),
          Step(TEXT, type_text("detached work") + ENTER, "commit message"),
          Step(PLAN, b"q", "q at the plan")], timeout=60)],
      watch="The rescue only decides: the new branch is the plan's first step, so q at the plan "
            "leaves no branch, HEAD still detached and nothing staged — and 'nothing was done' "
            "is then true (F6).")
def c_m46(fx, r):
    plan = plan_block(snap(r[0], "q at the plan"))
    return [exit_is(r[0], 1), shows(r[0], "Canceled"),
            ok("no new branch", fx.branches() == fx.vars["branches"], str(fx.branches())),
            ok("HEAD still detached", fx.git("symbolic-ref", "-q", "HEAD", check=False) == ""),
            ok("HEAD still at the same commit", fx.head() == fx.vars["head"]),
            ok("index unchanged (nothing staged)", fx.git("diff", "--cached", "--name-only") == ""),
            ok("git status unchanged (the edit still there, unstaged)",
               fx.status() == fx.vars["status"], fx.status()),
            ok("the plan shows the branch creation", "kept-work" in plan, plan),
            no_crash(r[0])]


def s_m47(fx):
    fx.sandbox()
    fx.write("app.txt", "an edit\n", append=True)
    fx.vars["status"] = fx.status()


@test(id="M-47", title="Bring back a stash when there is none: plain message, exit 1",
      part="1 · Everyday", setup=s_m47, since="v0.5",
      runs=[Run(["stash pop"], steps=[
          Step(PLAN, ENTER, "v0.4 flow: a plan for a pop that can't work", optional=True)],
                timeout=30)],
      watch="Blocked before any plan, in plain words (F4); no libgit2 'refs/stash' error chain; "
            "the uncommitted edit untouched.")
def c_m47(fx, r):
    return [exit_is(r[0], 1),
            says(r[0], "There are no stashed changes to bring back."),  # copy: plan wording
            lacks(r[0], PLAN, "blocked before any plan"),
            ok("the working tree is untouched", fx.status() == fx.vars["status"], fx.status()),
            no_crash(r[0])]
