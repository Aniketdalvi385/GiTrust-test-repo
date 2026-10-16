#!/usr/bin/env python3
"""Whole-system eval: what does GiTrust DO with each request?

Every request runs as `gitrust --yes "<request>"` in a fresh throwaway repo (a bare
remote, a pushed main, two edited files — the realistic "dirty" state; the same on a
pushed `feature` branch that main has moved past, for requests that bring main into
"my branch" (situation "feature", from v0.5.0); or a repo stopped mid-rebase /
mid-merge for in-progress cases), with GITRUST_DEBUG=1 so the
model's ranking is printed. All deterministic layers are included: exact phrases,
learned phrases (none here), Kev's confidence bars, the request-words cross-check,
the reversed-order re-ask for destructive operations, the "not Git" bar.

Outcomes:
  instant-right / instant-WRONG   an exact phrase matched (no model)
  acted-right / acted-WRONG       Kev was confident and GiTrust acted on its own
  asked                           GiTrust asked with a menu (under --yes: refused)
  refused-right / refused-WRONG   "not a Git request"
  other                           anything else (printed, review it)

A wrong action is also classed by blast radius: READ_ONLY ops can't change anything.

Sets (eval/sets/): v1_44 (the 2026-08 paper set), v2_owner_68 (the owner's own
phrasings, 2026-10-14), v3_blind (written 2026-10-15 by three persona agents who never
saw the training data, labels checked by an independent annotator). None were trained on.

Needs a Kev server on :8009. Usage:
  python3 eval/run_eval.py <version> [set …]          # default: all three sets
"""
import json, os, re, subprocess, sys, tempfile, time, urllib.request
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(HERE)
BIN = os.environ.get("GITRUST_BIN", os.path.abspath(os.path.join(
    REPO_ROOT, "..", "Glit", "gitrust", "target", "release", "gitrust")))
URL = os.environ.get("KEV_URL", "http://127.0.0.1:8009")
CONTROL = {"rebase_continue", "rebase_skip", "rebase_abort", "merge_abort",
           "cherry_pick_continue", "cherry_pick_abort", "revert_continue", "revert_abort"}
READ_ONLY = {"status", "log", "diff", "branches", "config", "show", "fetch", "merge_preview",
             "remotes", "find_lost_work"}

# Engine-line title (ux::intent_title) → op, for exact-phrase hits (no model ranking).
TITLES = [("Show status", "status"), ("Show history", "log"), ("Show changes", "diff"),
          ("List remotes", "remotes"), ("List branches", "branches"),
          ("Show Git settings", "config"), ("Show commit", "show"), ("Show the last commit", "show"),
          ("Check ", "fetch"), ("Preview a pull", "merge_preview"), ("Stage files", "add_commit"),
          ("Commit staged files", "commit"), ("Create branch", "branch"), ("Switch to", "checkout"),
          ("Stash changes", "stash"), ("Restore stashed", "stash_pop"), ("Pull from", "pull"),
          ("Start a repository", "init"), ("Remove Git", "delete_repo"),
          ("Add remote", "add_remote"), ("Remove remote", "remove_remote"),
          ("Commit and push", "commit_push"), ("Commit ", "add_commit"),
          ("Push only", "scoped_push"), ("Push to", "push"), ("Undo the last", "undo"),
          ("Find lost work", "find_lost_work"), ("Discard uncommitted", "cleanup"),
          ("Reword the last", "amend"), ("Amend the last", "amend"), ("Revert", "revert"),
          ("Unstage", "unstage"), ("Track ", "set_upstream"), ("Squash", "squash"),
          ("Pull with rebase", "pull_rebase"), ("Force push", "force_push"),
          ("Reset to the remote", "discard_local"), ("Abort the merge", "merge_abort"),
          ("Continue the rebase", "rebase_continue"), ("Skip this commit", "rebase_skip"),
          ("Abort the rebase", "rebase_abort"), ("Update from ", "sync")]


def git(cwd, *a, check=True):
    return subprocess.run(["git", *a], cwd=cwd, check=check, capture_output=True, text=True)


def make_home(base):
    home = os.path.join(base, "home")
    os.makedirs(home)
    open(os.path.join(home, ".gitconfig"), "w").write(
        "[user]\n\tname = Eval\n\temail = eval@example.invalid\n[init]\n\tdefaultBranch = main\n")
    open(os.path.join(home, ".gitrust.toml"), "w").write(
        f'kev_url = "{URL}"\nkev_autostart = false\nkev_idle_minutes = 0\n')
    return home


def repo(base, env, situation):
    root = tempfile.mkdtemp(dir=base)
    bare, work = os.path.join(root, "remote.git"), os.path.join(root, "work")
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", bare], env=env, check=True)
    subprocess.run(["git", "clone", "-q", bare, work], env=env, check=True, capture_output=True)
    for f, c in (("api_client.py", "a\n"), ("login.py", "b\n"), ("README.md", "r\n")):
        open(os.path.join(work, f), "w").write(c)
    for args in (["add", "."], ["commit", "-qm", "initial"], ["push", "-q", "-u", "origin", "main"],
                 ["commit", "-q", "--allow-empty", "-m", "second"]):
        subprocess.run(["git", *args], cwd=work, env=env, check=True, capture_output=True)
    if situation == "feature":
        # On a pushed feature branch that main has moved past. "Sync with main" on
        # main itself has nothing to bring in, and v0.5.0 reads the real branches.
        for args in (["checkout", "-q", "-b", "feature"], ["push", "-q", "-u", "origin", "feature"],
                     ["checkout", "-q", "main"]):
            subprocess.run(["git", *args], cwd=work, env=env, check=True, capture_output=True)
        open(os.path.join(work, "README.md"), "a").write("main moves on\n")
        for args in (["commit", "-qam", "main moves on"], ["push", "-q", "origin", "main"],
                     ["checkout", "-q", "feature"]):
            subprocess.run(["git", *args], cwd=work, env=env, check=True, capture_output=True)
        situation = "normal"
    if situation == "normal":
        for f in ("api_client.py", "login.py"):
            open(os.path.join(work, f), "a").write("edit\n")
        return work
    run = lambda *a: subprocess.run(["git", *a], cwd=work, env=env, capture_output=True)  # noqa
    run("checkout", "-q", "-b", "feature")
    for i in (1, 2):
        open(os.path.join(work, "login.py"), "a").write(f"feature {i}\n")
        run("commit", "-qam", f"feature {i}")
    run("checkout", "-q", "main")
    open(os.path.join(work, "login.py"), "a").write("main change\n")
    run("commit", "-qam", "main change")
    if situation == "rebase":
        run("checkout", "-q", "feature")
        r = run("rebase", "main")
    elif situation == "cherry_pick":
        r = run("cherry-pick", "feature~1")
    else:
        r = run("merge", "feature")
    assert r.returncode != 0, f"expected a {situation} conflict"
    return work


def classify(text):
    """-> (outcome, op GiTrust went for, kev's top op)."""
    kev = re.search(r"\(kev(?: in-progress)?: (\S+?)=", text)
    top = kev.group(1) if kev else None
    if "(fast-path:" in text:
        for line in text.splitlines():
            for prefix, op in TITLES:
                t = line.lstrip("+*⚡✦◇ ").strip()
                if t.startswith(prefix) and "(fast-path" not in line:
                    return "instant", op, top
        return "instant", None, top
    if "doesn't look like a Git request" in text:
        return "refused", "__reject__", top
    if "won't choose for you" in text or "cannot answer this choice" in text:
        return "asked", None, top
    if re.search(r"\(p=\d", text) or "· learned" in text:
        return "acted", top, top
    if top and re.search(r"Couldn't find .* in your request", text):
        # Routed (the engine line was printed), then an argument (topic, branch name,
        # count) wasn't in the words: under --yes that's an error, interactively a question.
        return "acted+arg-asked", top, top
    if "In progress" in text or "in progress —" in text:
        return "instant", "status", top            # the mid-operation status rule
    return "other", None, top


def score(rows):
    tally = Counter(r["outcome"] for r in rows)
    n = len(rows)
    right = sum(v for k, v in tally.items() if "right" in k)
    return {"n": n, "tally": dict(tally), "right": right, "asked": tally["asked"],
            "arg_asked": sum(v for k, v in tally.items() if "arg-asked" in k),
            "wrong_changes_something": sum(v for k, v in tally.items()
                                           if "changes something" in k)}


def rescore(version):
    """Re-classify saved rows (no binary run): python3 eval/run_eval.py --rescore 0.4.1"""
    out_dir = os.path.join(REPO_ROOT, "runs", f"v{version}", "eval")
    summary = json.load(open(os.path.join(out_dir, "summary.json")))
    for name in summary["sets"]:
        path = os.path.join(out_dir, f"{name}.json")
        d = json.load(open(path))
        for r in d["rows"]:
            if r["outcome"] != "other":
                continue
            kind, op, top = classify(r["output"])
            if kind in ("instant", "acted", "acted+arg-asked", "refused"):
                ok_ = op in r["accept"] or ("something_else" in r["accept"] and op not in CONTROL)
                kind = f"{kind}-{'right' if ok_ else 'WRONG'}"
            r["outcome"], r["op"] = kind, op or r["op"]
        d.update(score(d["rows"]))
        json.dump(d, open(path, "w"), indent=1, ensure_ascii=False)
        summary["sets"][name] = {k: d[k] for k in ("n", "tally", "right", "asked", "arg_asked",
                                                   "wrong_changes_something")}
        print(name, summary["sets"][name])
    json.dump(summary, open(os.path.join(out_dir, "summary.json"), "w"), indent=1)


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--rescore":
        return rescore(sys.argv[2])
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    version, sets = sys.argv[1], sys.argv[2:] or ["v1_44", "v2_owner_68", "v3_blind"]
    m = json.loads(urllib.request.urlopen(URL + "/v1/models").read())["models"][0]
    out_dir = os.path.join(REPO_ROOT, "runs", f"v{version}", "eval")
    os.makedirs(out_dir, exist_ok=True)
    base = tempfile.mkdtemp(prefix="gitrust-eval-")
    home = make_home(base)
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(HOME=home, GITRUST_DEBUG="1", NO_COLOR="1", GIT_TERMINAL_PROMPT="0")
    summary = {"model": m["run"], "temperature": m["temperature"], "binary": BIN, "sets": {}}
    for name in sets:
        cases = json.load(open(os.path.join(HERE, "sets", f"{name}.json")))["cases"]
        rows, tally = [], Counter()
        t0 = time.time()
        for c in cases:
            accept = c["accept"]
            work = repo(base, env, c.get("situation", "normal"))
            p = subprocess.run([BIN, "--yes", c["q"]], cwd=work, env=env, capture_output=True,
                               text=True, timeout=180)
            out = p.stdout + p.stderr
            kind, op, top = classify(out)
            if kind in ("instant", "acted", "acted+arg-asked", "refused"):
                right = op in accept or ("something_else" in accept and op not in CONTROL)
                kind = f"{kind}-{'right' if right else 'WRONG'}"
                if kind.endswith("WRONG") and kind != "refused-WRONG":
                    kind += " (read-only)" if op in READ_ONLY else " (changes something)"
            tally[kind] += 1
            rows.append({"id": c.get("id"), "q": c["q"], "accept": accept,
                         "situation": c.get("situation", "normal"), "persona": c.get("persona"),
                         "outcome": kind, "op": op, "kev_top": top, "exit": p.returncode,
                         "output": out[-600:] if kind == "other" or "WRONG" in kind else ""})
            print(f"  {kind:36} {c['q'][:60]!r:62} want={'/'.join(accept)} got={op or top}",
                  flush=True)
        res = dict(score(rows), seconds=round(time.time() - t0))
        n, right, wrong_change = res["n"], res["right"], res["wrong_changes_something"]
        summary["sets"][name] = res
        json.dump({"set": name, "model": m["run"], "rows": rows, **res},
                  open(os.path.join(out_dir, f"{name}.json"), "w"), indent=1, ensure_ascii=False)
        print(f"\n{name}: n={n}  right={right} ({right / n:.0%})  asked={tally['asked']}  "
              f"wrong-that-changes-something={wrong_change}  {dict(tally)}\n")
    json.dump(summary, open(os.path.join(out_dir, "summary.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
