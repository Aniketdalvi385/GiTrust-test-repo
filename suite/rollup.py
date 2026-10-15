#!/usr/bin/env python3
"""Build runs/v<version>/README.md (index) from the per-test records and the eval summary.

Verdict per test = the reviewer's verdict if results/<id>/review.md starts with
"Verdict: …", otherwise the automatic one. REPORT.md (the narrative) is written by
hand / by the reviewing agent; this script only builds the index tables.

  python3 suite/rollup.py 0.4.1
"""
import json, os, re, sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
ICON = {"PASS": "✅", "PASS-WITH-NOTES": "⚠️", "FAIL": "❌", "BLOCKED": "⛔", "SKIP": "⏭️"}


def verdict(d):
    rec = json.load(open(os.path.join(d, "result.json")))
    rv = os.path.join(d, "review.md")
    v = rec["auto_verdict"]
    note = ""
    if os.path.exists(rv):
        text = open(rv).read()
        m = re.search(r"^Verdict:\s*([A-Z-]+)", text, re.M)
        if m:
            v = m.group(1)
        n = re.search(r"^Summary:\s*(.+)$", text, re.M)
        note = n.group(1).strip() if n else ""
    return rec, v, note


def main():
    version = sys.argv[1]
    run_dir = os.path.join(REPO_ROOT, "runs", f"v{version}")
    res = os.path.join(run_dir, "results")
    rows, tally = [], {}
    for tid in sorted(os.listdir(res)):
        d = os.path.join(res, tid)
        if not os.path.exists(os.path.join(d, "result.json")):
            continue
        rec, v, note = verdict(d)
        tally[v] = tally.get(v, 0) + 1
        rows.append((rec, v, note))
    env = json.load(open(os.path.join(run_dir, "environment.json")))
    lines = [f"# GiTrust v{version} — acceptance run", "",
             f"- **Binary:** `gitrust {env.get('binary_version')}`",
             f"- **Model:** `{env.get('kev', {}).get('run', '?')}` "
             f"(T={env.get('kev', {}).get('temperature', '?')})",
             "- **How:** `suite/run.py auto` — a pseudo-terminal drives the release binary, "
             "presses the keys each test lists, then checks exit code, repository and screen; "
             "every result was then reviewed from its screens (`review.md`). ★ = flagship, "
             "also run by hand (`suite/run.py manual`).",
             "- **Report:** [REPORT.md](REPORT.md)", "",
             "**Result:** " + " · ".join(f"{n} {ICON.get(k, k)} {k}" for k, n in sorted(tally.items())),
             "", "| ID | Test | Since | Mode | Result | Note |", "|---|---|---|---|---|---|"]
    for rec, v, note in rows:
        lines.append(f"| [{rec['id']}](results/{rec['id']}/) | {rec['title']}"
                     f"{' ★' if rec['flagship'] else ''} | {rec['since']} | {rec['mode']} | "
                     f"{ICON.get(v, '')} {v} | {note} |")
    summ = os.path.join(run_dir, "eval", "summary.json")
    if os.path.exists(summ):
        s = json.load(open(summ))
        lines += ["", "## Eval (whole system, `gitrust --yes`, dirty repo)", "",
                  f"Model `{s['model']}`. Details: [eval/](eval/).", "",
                  "| Set | n | right | asked (menu) | wrong, read-only | wrong, changes something |",
                  "|---|---|---|---|---|---|"]
        for name, r in s["sets"].items():
            t = r["tally"]
            ro = sum(v for k, v in t.items() if "read-only" in k)
            lines.append(f"| {name} | {r['n']} | {r['right']} ({r['right'] / r['n']:.0%}) | "
                         f"{r['asked']} | {ro} | {r['wrong_changes_something']} |")
    open(os.path.join(run_dir, "README.md"), "w").write("\n".join(lines) + "\n")
    print(" · ".join(f"{k}={n}" for k, n in sorted(tally.items())))


if __name__ == "__main__":
    main()
