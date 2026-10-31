#!/usr/bin/env python3
"""Calibration of the shipped Kev model on the 338-request blind set (added 2026-10-31).

Asks Kev each blind request the way GiTrust v0.5.0 does — same options, same order, same
state — and scores the probability of its top answer: ECE (10 equal-width bins), Brier, and a
reliability diagram (SVG). Model level only: no exact phrases, no checks, no menus.

- State: {"user_request", "repo_state"}; the repo-state lines below were captured from the
  release binary in each eval fixture (a stand-in Kev server recorded its requests).
- Mid-rebase / mid-merge: GiTrust first asks the family question (continue / skip / abort /
  something_else). Its target is the accepted control op, else `something_else`; when the
  right answer is `something_else`, GiTrust goes on to the main question, so that is scored too.
- Several accepted answers: the top answer is right if it is any of them. The multi-class
  Brier uses a one-hot on the accepted answer Kev gave the most probability.

  python3 eval/calibration.py [--gitrust <Glit checkout>]      # needs Kev on :8009 at T=4.0
"""
import datetime, json, math, os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
GLIT = sys.argv[sys.argv.index("--gitrust") + 1] if "--gitrust" in sys.argv else os.path.join(HERE, "..", "..", "Glit")
KEV = os.environ.get("KEV_URL", "http://127.0.0.1:8009")
TODAY = datetime.date.today().isoformat()
OUT = os.path.join(HERE, "..", "runs", "v0.5.0", "eval", f"calibration_{TODAY}")
STATES = {"normal": "on branch main, 2 files modified, 1 commit ahead of origin",
          "feature": "on branch feature, 2 files modified",
          "rebase": "detached HEAD, rebase in progress (1/2, conflicts in 1 file(s))",
          "merge": "on branch main, 2 commits ahead of origin, merge in progress (conflicts in 1 file(s))"}

OPS = json.load(open(os.path.join(GLIT, "gitrust", "src", "kev_ops.json")))
FAMILY = {f: ops + [OPS["in_progress"]["other"]] for f, ops in OPS["in_progress"]["families"].items()}


def ask(state, instructions, options):
    body = {"model": "kev-latest", "state": state, "questions": {"op": {
        "type": "choice", "instructions": instructions, "criteria": {o: d for o, d in options}}}}
    req = urllib.request.Request(KEV + "/v1/systemone", json.dumps(body).encode(), {"content-type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=120).read())["answers"]["op"]["probabilities"]


def sample(case, kind, probs, targets):
    top = max(probs, key=probs.get)
    best = max(targets, key=lambda t: probs.get(t, 0.0))
    return {"id": case["id"], "kind": kind, "ambiguous": case.get("ambiguous", False), "targets": sorted(targets),
            "top": top, "conf": probs[top], "correct": top in targets, "p_targets": sum(probs.get(t, 0) for t in targets),
            "brier_multi": sum((p - (o == best)) ** 2 for o, p in probs.items())}


def metrics(rows, bins=10):
    n = len(rows)
    table = []
    for b in range(bins):
        inb = [r for r in rows if min(int(r["conf"] * bins), bins - 1) == b]
        if inb:
            table.append({"bin": f"{b / bins:.1f}-{(b + 1) / bins:.1f}", "n": len(inb),
                          "confidence": sum(r["conf"] for r in inb) / len(inb),
                          "accuracy": sum(r["correct"] for r in inb) / len(inb)})
    return {"n": n, "accuracy": sum(r["correct"] for r in rows) / n,
            "mean_confidence": sum(r["conf"] for r in rows) / n,
            "ece": sum(t["n"] / n * abs(t["accuracy"] - t["confidence"]) for t in table),
            "brier_top_label": sum((r["conf"] - r["correct"]) ** 2 for r in rows) / n,
            "brier_multiclass": sum(r["brier_multi"] for r in rows) / n,
            "nll_accepted_set": -sum(math.log(max(r["p_targets"], 1e-6)) for r in rows) / n, "bins": table}


def svg(table, m):
    x, y = (lambda v: 60 + v * 400), (lambda v: 440 - v * 400)
    bars = "".join(f'<rect x="{x(i / 10) + 4}" y="{y(t["accuracy"])}" width="32" height="{440 - y(t["accuracy"])}" fill="#4a7fd0" fill-opacity="0.8"/>'
                   f'<circle cx="{x(t["confidence"])}" cy="{y(t["accuracy"])}" r="3" fill="#1f3f73"/>'
                   f'<text x="{x(i / 10) + 20}" y="456" font-size="10" text-anchor="middle">n={t["n"]}</text>'
                   for i, t in ((int(float(t["bin"][:3]) * 10), t) for t in table))
    ticks = "".join(f'<text x="{x(v / 10)}" y="474" font-size="11" text-anchor="middle">{v / 10:.1f}</text>'
                    f'<text x="52" y="{y(v / 10) + 4}" font-size="11" text-anchor="end">{v / 10:.1f}</text>' for v in range(0, 11, 2))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 510" font-family="sans-serif">'
            f'<rect width="500" height="510" fill="white"/><text x="60" y="24" font-size="14" font-weight="600">'
            f'Kev gitrust-v2 (T = 4.0), blind set: ECE {m["ece"]:.3f}, Brier {m["brier_top_label"]:.3f}</text>'
            f'<line x1="{x(0)}" y1="{y(0)}" x2="{x(1)}" y2="{y(1)}" stroke="#999" stroke-dasharray="4 4"/>'
            f'<rect x="60" y="40" width="400" height="400" fill="none" stroke="#666"/>{bars}{ticks}'
            f'<text x="260" y="498" font-size="12" text-anchor="middle">confidence of the top answer (bars: accuracy per bin; dot: mean confidence)</text></svg>')


def main():
    info = json.loads(urllib.request.urlopen(KEV + "/v1/models").read())["models"][0]
    assert abs(info["temperature"] - 4.0) < 1e-6 and "gitrust-kev-0.8b@v2" in info["run"], info
    for p in (OUT + ".json", OUT + ".svg"):
        if os.path.exists(p):
            sys.exit(f"refusing to overwrite {p}")
    main_opts = [tuple(o) for o in OPS["ops"]]
    rows = []
    for c in json.load(open(os.path.join(HERE, "sets", "v3_blind.json")))["cases"]:
        sit = c.get("situation", "normal")
        state = {"user_request": c["q"], "repo_state": STATES[sit]}
        to_main = True
        if sit in FAMILY:
            fam = [tuple(o) for o in FAMILY[sit]]
            ctrl = set(c["accept"]) & {o for o, _ in fam}
            rows.append(sample(c, "in_progress", ask(state, OPS["in_progress"]["instructions"], fam), ctrl or {fam[-1][0]}))
            to_main = not ctrl
        if to_main:
            assert set(c["accept"]) <= {o for o, _ in main_opts}, c
            rows.append(sample(c, "routing", ask(state, OPS["instructions"], main_opts), set(c["accept"])))
        print(f'{len(rows):3} {rows[-1]["kind"]:11} {"ok  " if rows[-1]["correct"] else "MISS"} {rows[-1]["conf"]:.2f} {c["q"][:60]}', flush=True)
    report = {"date": TODAY, "model": info["run"], "temperature": info["temperature"], "states": STATES,
              "all": metrics(rows), "routing": metrics([r for r in rows if r["kind"] == "routing"]),
              "in_progress": metrics([r for r in rows if r["kind"] == "in_progress"]),
              "unambiguous": metrics([r for r in rows if not r["ambiguous"]]), "rows": rows}
    json.dump(report, open(OUT + ".json", "w"), indent=1)
    open(OUT + ".svg", "w").write(svg(report["all"]["bins"], report["all"]))
    print(json.dumps({k: {m: v for m, v in report[k].items() if m != "bins"} for k in ("all", "routing", "in_progress", "unambiguous")}, indent=1))
    print("wrote", OUT + ".json", OUT + ".svg")


if __name__ == "__main__":
    main()
