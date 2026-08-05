# M-25 · Empty-scan honesty

| | |
|---|---|
| **LLM** | no |
| **Flagship** | — |
| **Result** | ✅ PASS |
| **Run date** | 2026-08-04 |

## What this proves

Honest gc/never-committed caveat.

## Procedure

**Setup:** fresh `mk_sandbox m25`, nothing lost.

**Steps:**
```bash
$GITRUST "find my lost work"
```

**Expect:** empty-result message includes the honest caveat about never-committed / garbage-collected work being possibly unrecoverable — not a bare "nothing found".

## Result

**✅ PASS — empty scan is honest (S29). Carries the gc/never-committed caveat verbatim.**

**Setup:** fresh `m25` sandbox, only `base` commit, nothing dangling.

**Result:** `gitrust "find my lost work"` returned:
> *"Nothing found. Work that was never committed, or that git has already garbage-collected, may be unrecoverable."*

- Reports nothing found (correct — nothing lost). ✅
- **Exact S29 honesty caveat** — names both *never committed* and *garbage-collected* as possibly unrecoverable, matching the plan's specified copy word-for-word. ✅
- Not a bare "nothing found"; does not falsely imply a clean bill of health. ✅
- `EXIT=0` — correct (a successful scan that found nothing; the systemic exit-0 bug only concerns failure/refusal paths).

The honesty rule was implemented deliberately and correctly. Consistent with M-23/M-24 — the recovery subsystem is the tool's strongest area.

**Repro:** deterministic.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
