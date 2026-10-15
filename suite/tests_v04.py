"""The GiTrust acceptance suite for v0.4+ as data (see gitrust_suite.py).

M-00…M-30 keep the ids and intent of the original 31-test suite (MANUAL_TEST_SUITE.md,
v0.2/v0.3), so results compare across versions; their expectations are updated for
v0.4 (Kev instead of Ollama, user-written commit messages, every cancel exits 1).
M-31 onwards are new in v0.4: the UX conventions and the model's behaviour.

Waiting on screen text: "[Enter] run" = the plan prompt; "Esc to cancel" = a text
prompt; "Esc cancel" = a menu. Menu options are chosen by label (`pick`), never by
position.
"""
import os

from gitrust_suite import (BACKSPACE, CTRL_C, ENTER, ESC, Run, Step, Test, confirm_typed,
                           accept_prefilled, exit_is, if_menu, lacks, no_crash, ok, pick, shows, type_text)

PLAN = "[Enter] run"
TEXT = "Esc to cancel"
MENU = "Esc cancel"
CANCELED = "Canceled — nothing was done."

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
      runs=[Run(["push the login changes"], steps=[
          maybe_menu("Push only some changes", "Stage which files"),
          Step("Stage which files", ENTER, "file picker"),
          Step(TEXT, type_text("login page") + ENTER, "commit message"),
          Step(PLAN, ENTER, "plan")], timeout=150)],
      watch="Picker pre-selects the login files, shows +N −M and a reason per file; readme.txt "
            "not pre-selected; only login files reach the remote.")
def c_m04(fx, r):
    pushed = fx.git("show", "--name-only", "--format=", "origin/main", check=False).split()
    return [exit_is(r[0], 0), ok("login.txt pushed", "login.txt" in pushed, str(pushed)),
            ok("readme.txt NOT pushed", "readme.txt" not in pushed, str(pushed)),
            ok("readme.txt still uncommitted", "readme.txt" in fx.status(), fx.status()),
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
            Run(["switch to other"], steps=[Step(PLAN, ENTER, optional=True)], timeout=40)],
      watch="Branch created; switching back with uncommitted edits either works safely or is "
            "refused with a clear reason — never a crash, never lost edits.")
def c_m05(fx, r):
    edit_kept = "my uncommitted edit" in (fx.read("app.txt") or "")
    return [exit_is(r[0], 0, "branch created (exit 0)"),
            ok("feature-x exists", "feature-x" in fx.git("branch", "--list")),
            ok("the uncommitted edit survives the switch attempt", edit_kept),
            ok("a refused switch does not exit 0",
               r[1].exit != 0 or fx.git("branch", "--show-current") == "other",
               f"exit={r[1].exit} on={fx.git('branch', '--show-current')}"),
            no_crash(r[0]), no_crash(r[1])]


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
      watch="The rebase/merge choice explains both in plain words; rebase + push in one go.")
def c_m06(fx, r):
    log = fx.git("log", "--format=%s")
    return [exit_is(r[0], 0), ok("in sync with origin (0 0)", fx.ahead_behind() == (0, 0),
                                 str(fx.ahead_behind())),
            ok("teammate commit below mine", log.index("feat: mine") < log.index("teammate"), log),
            ok("linear history (no merge commit)",
               len(fx.git("log", "-1", "--format=%P").split()) == 1), no_crash(r[0])]


@test(id="M-07", title="Diverged push → merge", part="2 · Divergence", setup=s_diverged,
      since="v0.2",
      runs=[Run(["push"], steps=[Step(MENU, pick("erge"), "reconcile choice"),
                                 Step(PLAN, ENTER, "plan")], timeout=90)],
      watch="Merge path: a merge commit, then pushed.")
def c_m07(fx, r):
    return [exit_is(r[0], 0), ok("in sync with origin (0 0)", fx.ahead_behind() == (0, 0),
                                 str(fx.ahead_behind())),
            ok("merge commit has 2 parents",
               len(fx.git("log", "-1", "--format=%P").split()) == 2), no_crash(r[0])]


def s_conflict(fx):
    fx.sandbox()
    fx.teammate_pushes(rel="app.txt", text="teammate line\n", msg="teammate: app")
    fx.commit("app.txt", "my line\n", "feat: my app change")
    fx.git("fetch", "-q")
    fx.vars["pre"] = fx.head()


@test(id="M-08", title="Rebase conflict → calm pause → continue", part="2 · Divergence",
      setup=s_conflict, since="v0.2",
      runs=[Run(["push"], steps=[Step(MENU, pick("ebase")), Step(PLAN, ENTER)], timeout=90)],
      watch="Pause message names the file, says nothing is lost, names continue/abort; exit ≠ 0.")
def c_m08(fx, r):
    s = r[0].screen
    checks = [ok("paused with a non-zero exit", r[0].exit not in (0, None), f"exit={r[0].exit}"),
              shows(r[0], "nothing is lost"), shows(r[0], "continue rebase"),
              ok("git is mid-rebase", os.path.isdir(os.path.join(fx.work, ".git", "rebase-merge"))
                 or os.path.isdir(os.path.join(fx.work, ".git", "rebase-apply"))), no_crash(r[0])]
    # Resolve and continue through gitrust (exact phrase, no model).
    fx.write("app.txt", "base\nteammate line\nmy line\n")
    fx.git("add", "app.txt")
    from gitrust_suite import execute
    r2 = execute(fx, Run(["continue rebase"], steps=[Step(PLAN, ENTER)], timeout=60))
    r.append(r2)
    checks += [exit_is(r2, 0, "continue rebase exits 0"),
               ok("rebase finished", not os.path.isdir(os.path.join(fx.work, ".git",
                                                                    "rebase-merge"))),
               no_crash(r2)]
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
      watch="Target resolves to main; rebase on an unpublished branch needs no force push.")
def c_m10(fx, r):
    return [exit_is(r[0], 0), ok("feature contains main's commit",
                                 fx.git("merge-base", "--is-ancestor", "origin/main", "HEAD",
                                        check=False) == "" and
                                 "main: moved" in fx.git("log", "--format=%s")),
            lacks(r[0], "--force ", "no bare --force"), no_crash(r[0])]


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
          Step(MENU, pick("ranch"), "rescue choice"), Step(TEXT, type_text("rescued") + ENTER),
          maybe_prefilled(), Step(PLAN, ENTER)], timeout=60)],
      watch="Not a dead end: offers to make a branch here; the work ends up on it.")
def c_m13(fx, r):
    return [ok("now on a branch", fx.git("symbolic-ref", "-q", "--short", "HEAD", check=False) != ""),
            no_crash(r[0])]


def s_m14(fx):
    fx.sandbox()
    fx.git("checkout", "-q", fx.head())
    fx.vars["detached"] = fx.commit("app.txt", "y\n", "detached work")


@test(id="M-14", title="Switching away would strand a commit → guard", part="3 · Stuck states",
      setup=s_m14, flagship=False, since="v0.2",
      runs=[Run(["checkout main"], steps=[Step(MENU, pick("ranch")),
                                          Step(TEXT, type_text("saved-work") + ENTER),
                                          Step(PLAN, ENTER)], timeout=60)],
      watch="Says the commit would be stranded and offers a branch first; nothing lost.")
def c_m14(fx, r):
    reach = fx.git("branch", "--contains", fx.vars["detached"], check=False)
    return [ok("the detached commit is on a branch", reach.strip() != "", reach), no_crash(r[0])]


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
      runs=[Run(["undo"], steps=[Step(MENU, pick("throw the changes away")),
                                 Step("to confirm", confirm_typed(), "type to confirm"),
                                 Step(PLAN, ENTER)])],
      watch="A typed confirmation before anything happens; the success line names the backup.")
def c_m16(fx, r):
    return [exit_is(r[0], 0), ok("commit gone", fx.head() == fx.vars["before"]),
            ok("working tree clean", fx.status() == "", fx.status()),
            ok("trash backup written", any("app.txt" in t for t in fx.trash_files()),
               str(fx.trash_files())), shows(r[0], "backup"), no_crash(r[0])]


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
      watch="Guidance (squash / revert / undo one); nothing changes.")
def c_m18(fx, r):
    return [exit_is(r[0], 1), ok("HEAD unchanged", fx.head() == fx.vars["tip"]),
            shows(r[0], "squash"), no_crash(r[0])]


@test(id="M-19", title="Squash last 3: same content, one commit", part="4 · Undo",
      setup=s_three, needs_model=True, since="v0.2",
      runs=[Run(["squash the last 3 commits"], steps=[
          maybe_menu("Squash commits", TEXT),
          Step(TEXT, type_text("three in one") + ENTER, "message"),
          Step(PLAN, ENTER)], timeout=60)],
      watch="Asks for the squashed message; tree identical afterwards.")
def c_m19(fx, r):
    return [exit_is(r[0], 0), ok("2 fewer commits", fx.count() == 2, str(fx.count())),
            ok("tree identical", fx.git("rev-parse", "HEAD^{tree}") == fx.vars["tree"]),
            no_crash(r[0])]


def s_m20(fx):
    fx.sandbox()
    fx.commit("app.txt", "v2\n", "typo mesage")
    fx.git("push", "-q")


@test(id="M-20", title="Fix a pushed commit's message: escalate + lease", part="4 · Undo",
      setup=s_m20, needs_model=True, flagship=False, since="v0.2",
      runs=[Run(["fix the last commit message to 'typo message fixed'"], steps=[
          maybe_menu("Amend the last commit", "to confirm"),
          Step("to confirm", confirm_typed(), "type to confirm"),
          Step(PLAN, ENTER)], timeout=90)],
      watch="Explains a force push is needed; typed confirmation; uses --force-with-lease.")
def c_m20(fx, r):
    return [exit_is(r[0], 0), ok("message fixed on the remote",
                                 fx.git("log", "-1", "--format=%s", "origin/main") ==
                                 "typo message fixed"),
            ok("remote == local", fx.git("rev-parse", "origin/main") == fx.head()),
            lacks(r[0], "--force "), no_crash(r[0])]


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
          Step("Pick one", ESC, "after the hook failed", optional=True)],
                timeout=60)],
      watch="Says hooks were detected; the hook's output is shown; nothing committed; exit ≠ 0. "
            "Note: after the failure a 'Pick one: Show / Cancel' menu appears.")
def c_m21(fx, r):
    return [ok("non-zero exit", r[0].exit not in (0, None), f"exit={r[0].exit}"),
            shows(r[0], "LINT FAILED"), ok("no new commit", fx.count() == fx.vars["count"]),
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
      runs=[Run(["revert last commit"], steps=[Step((PLAN, "(Y/n)"), b"y\r", "revert's own question"),
                                                Step(PLAN, ENTER, "plan")], timeout=60)],
      watch="Matches git: revert doesn't run pre-commit, so it succeeds. Note: revert asks its "
            "own (Y/n) question instead of the one-key plan prompt every other operation uses.")
def c_m22(fx, r):
    return [exit_is(r[0], 0), ok("one new (revert) commit", fx.count() == fx.vars["count"] + 1),
            ok("other.txt gone", fx.read("other.txt") is None), no_crash(r[0])]


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
      watch="The dropped stash is listed and can be restored to a branch.")
def c_m24(fx, r):
    rescue = [b.strip(" *") for b in fx.git("branch", "--list", "rescue/*").splitlines()]
    has = rescue and "wip" in fx.git("show", f"{rescue[0]}:app.txt", check=False)
    return [exit_is(r[0], 0), ok("rescue branch has the wip change", bool(has), str(rescue)),
            no_crash(r[0])]


@test(id="M-25", title="Nothing lost: an honest empty result", part="6 · Forensics",
      setup=s_none, since="v0.2", runs=[Run(["find my lost work"], timeout=40)],
      watch="Says nothing was found and why some work can't be recovered.")
def c_m25(fx, r):
    return [shows(r[0], "may be unrecoverable"), no_crash(r[0])]


def s_m26(fx):
    fx.sandbox()
    fx.write("app.txt", "mod\n", append=True)
    fx.write("junk/inner/file.txt", "tmp\n")


@test(id="M-26", title="Clean up: counts, untracked deleted, backed up", part="6 · Forensics",
      setup=s_m26, since="v0.2",
      runs=[Run(["clean up my repo"], steps=[Step(MENU, pick("untracked"), "clean-up choice"),
                                             Step(("to confirm", PLAN), confirm_typed(), optional=True),
                                             Step(PLAN, ENTER)], timeout=60)],
      watch="Gate shows how many files of each kind and names the backup. Note: deleting "
            "untracked files has no type-to-confirm (only the ⛔ plan + Enter) — the backup is "
            "their only copy.")
def c_m26(fx, r):
    return [exit_is(r[0], 0), ok("junk/ deleted", not os.path.exists(os.path.join(fx.work, "junk"))),
            ok("backup holds junk/inner/file.txt",
               any(t.endswith("junk/inner/file.txt") for t in fx.trash_files()),
               str(fx.trash_files())),
            ok("tracked edit untouched", "mod" in (fx.read("app.txt") or "")), no_crash(r[0])]


def s_m27(fx):
    fx.sandbox()
    fx.write("keep-me.txt", "untracked\n")
    t = os.path.join(fx.home, ".gitrust", "trash")
    os.makedirs(t)
    os.chmod(t, 0)


@test(id="M-27", title="Backup can't be written → nothing deleted", part="6 · Forensics",
      setup=s_m27, since="v0.2",
      runs=[Run(["clean up my repo"], steps=[Step(MENU, pick("untracked")),
                                             Step(("to confirm", PLAN), confirm_typed(), optional=True),
                                             Step(PLAN, ENTER)], timeout=60)],
      watch="Refuses, names the backup failure; the file still exists.")
def c_m27(fx, r):
    return [ok("non-zero exit", r[0].exit not in (0, None), f"exit={r[0].exit}"),
            ok("untracked file still there", fx.read("keep-me.txt") is not None), no_crash(r[0])]


@test(id="M-28", title="--recover with nothing to recover points to forensics",
      part="6 · Forensics", setup=s_none, since="v0.2", runs=[Run(["--recover"], mode="pipe")],
      watch="Says there's nothing interrupted and suggests 'find my lost work'.")
def c_m28(fx, r):
    return [shows(r[0], "find my lost work"), no_crash(r[0])]


# ============================================================ Part 7 — meta
@test(id="M-29", title="Model down: warning, full menu, refusals", part="7 · Meta",
      setup=s_none, since="v0.2",
      runs=[Run(["what changed in the auth files?"], model="down",
                steps=[Step(MENU, ESC, "manual menu")]),
            Run(["--yes", "what changed in the auth files?"], model="down", mode="pipe"),
            Run(["what changed"], model="down", mode="pipe", stdin="q\n"),
            Run(["status"], model="down")],
      watch="Warning names the fix; a menu of operations by title; --yes and no-terminal "
            "refuse with exit 1; status still instant.")
def c_m29(fx, r):
    return [shows(r[0], "isn't running"), ok("menu lists operations by title",
                                             "Show status" in (r[0].snaps[0][1] if r[0].snaps else "")),
            exit_is(r[0], 1, "Esc at the menu exits 1"), shows(r[0], CANCELED),
            exit_is(r[1], 1, "--yes refuses (exit 1)"), shows(r[1], "Choices"),
            exit_is(r[2], 1, "no terminal → exit 1"), shows(r[2], "no terminal to ask in"),
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
      watch="One readable line, no 'caused by'.")
def c_m38(fx, r):
    return [exit_is(r[0], 1), shows(r[0], "no terminal to ask in"), no_crash(r[0])]


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
      since="v0.4", runs=[Run(["--yes", "show history"], mode="pipe")],
      watch="(checked by the runner with a closed pipe — see check)")
def c_m41(fx, r):
    import subprocess
    from gitrust_suite import BIN
    p = subprocess.run(f"'{BIN}' --yes 'show history' | head -1", shell=True, cwd=fx.work,
                       env=fx.env(), capture_output=True, text=True)
    code = subprocess.run(f"'{BIN}' --yes 'show history' | head -1; exit ${{PIPESTATUS[0]}}",
                          shell=True, executable="/bin/bash", cwd=fx.work, env=fx.env(),
                          capture_output=True, text=True).returncode
    return [ok("no panic when the reader closes early", "panicked" not in p.stderr and code != 101,
               f"exit={code} stderr={p.stderr.strip()[:120]}")]


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
