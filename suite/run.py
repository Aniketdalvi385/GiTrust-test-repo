#!/usr/bin/env python3
"""Run the GiTrust acceptance suite. See gitrust_suite.py for what each mode does.

  python3 suite/run.py list
  uv run --with pyte python suite/run.py auto 0.5.0 [ids…]
  python3 suite/run.py manual 0.5.0 <id>

The tests (suite/tests.py) are the expectations of the release under test; older
releases' expectations are in git history (suite/README.md, "Versions").
"""
import json, os, sys, traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gitrust_suite as gs  # noqa: E402
from tests import TESTS  # noqa: E402


def select(ids):
    if not ids:
        return TESTS
    want = set(ids)
    picked = [t for t in TESTS if t.id in want]
    missing = want - {t.id for t in picked}
    if missing:
        sys.exit(f"unknown test id(s): {sorted(missing)}")
    return picked


def preflight(tests, version):
    run_dir = os.path.join(gs.REPO_ROOT, "runs", f"v{version}")
    os.makedirs(os.path.join(run_dir, "results"), exist_ok=True)
    bv = gs.binary_version()
    print(f"binary  {gs.BIN}  (version {bv})")
    if bv != version:
        print(f"  !  binary is {bv}, run folder is v{version}")
    if any(t.needs_model or any(r.model == "up" for r in t.runs) for t in tests):
        info = gs.kev_info()
        print(f"model   {info}")
        if "error" in info:
            print("  !  no Kev server on :8009 — model tests will fail. Start one first.")
    sc = gs.suite_commit()
    print(f"suite   {sc}")
    env = {"binary": gs.BIN, "binary_version": bv, "kev": gs.kev_info(), "suite_commit": sc}
    json.dump(env, open(os.path.join(run_dir, "environment.json"), "w"), indent=1)
    return run_dir


def run_auto(version, ids):
    shard = None
    if ids and ids[0].startswith("--shard="):          # --shard=i/n: every n-th test
        i, n = map(int, ids[0].split("=")[1].split("/"))
        shard, ids = (i, n), ids[1:]
    tests = select(ids)
    if shard:
        tests = tests[shard[0]::shard[1]]
    run_dir = preflight(tests, version)
    tally = {}
    for t in tests:
        fx = gs.Fixture(t.id)
        try:
            t.setup(fx)
            results = [gs.execute(fx, r) for r in t.runs]
            checks = t.check(fx, results)
        except Exception as e:  # noqa: BLE001
            results = locals().get("results", [])
            checks = [("test ran without a harness error", False,
                       f"{type(e).__name__}: {e} | {traceback.format_exc(limit=2)[-300:]}")]
        verdict = gs.write_record(run_dir, t, results, checks, "auto", fx)
        fx.cleanup()
        tally[verdict] = tally.get(verdict, 0) + 1
        failed = [c[0] for c in checks if not c[1]]
        print(f"  {'✅' if verdict == 'PASS' else '❌'} {t.id}  {t.title}"
              + (f"   ← {failed}" if failed else ""))
    print("  ".join(f"{k}={v}" for k, v in sorted(tally.items())))


def run_manual(version, ids):
    tests = select(ids)
    run_dir = preflight(tests, version)
    for t in tests:
        fx = gs.Fixture(t.id)
        print(f"\n=== {t.id} · {t.title}{'  ★' if t.flagship else ''}")
        print(f"    watch for: {t.watch}")
        t.setup(fx)
        print(f"    sandbox: {fx.work}")
        results = []
        import dataclasses
        t = dataclasses.replace(t, id=f"{t.id}-manual")   # kept beside the auto record
        rec_dir = os.path.join(run_dir, "results", t.id)
        os.makedirs(rec_dir, exist_ok=True)
        for i, r in enumerate(t.runs, 1):
            print(f"\n--- run {i}: gitrust {' '.join(repr(a) for a in r.argv)}"
                  f"{'   (model DOWN for this run)' if r.model == 'down' else ''}")
            if r.steps:
                print("    you'll be asked: " + " → ".join(s.label or s.wait or "…" for s in r.steps))
            input("    press Enter to start (you drive every prompt)… ")
            results.append(gs.execute_manual(fx, r, os.path.join(rec_dir, f"session-{i}.txt")))
            print(f"    (exit {results[-1].exit})")
        try:
            checks = t.check(fx, results)
        except Exception as e:  # noqa: BLE001
            checks = [("checks ran", False, f"{type(e).__name__}: {e}")]
        verdict = gs.write_record(run_dir, t, results, checks, "manual", fx)
        for n, o, d in checks:
            print(f"    {'✅' if o else '❌'} {n}" + (f"  ({d})" if d and not o else ""))
        print(f"    automatic checks: {verdict}  →  runs/v{version}/results/{t.id}/")
        fx.cleanup()


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("list", "auto", "manual"):
        sys.exit(__doc__)
    if sys.argv[1] == "list":
        for t in TESTS:
            print(f"{t.id}  {'★' if t.flagship else ' '} {'model' if t.needs_model else '     '}"
                  f"  {t.part:16}  {t.title}")
        return
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    (run_auto if sys.argv[1] == "auto" else run_manual)(sys.argv[2], sys.argv[3:])


if __name__ == "__main__":
    main()
