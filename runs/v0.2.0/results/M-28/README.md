# M-28 · Recover precedence: sideways pointer

| | |
|---|---|
| **LLM** | no |
| **Flagship** | — |
| **Result** | ✅ PASS |
| **Run date** | 2026-08-05 |

## What this proves

Points to find my lost work.

## Procedure

**Setup:** fresh `mk_sandbox m28`, no interrupted pipeline.

**Steps:**
```bash
$GITRUST --recover
```

**Expect:** "no interrupted pipeline" + the pointer to `gitrust "find my lost work"` — the two recovery worlds introduce each other.

## Result

**✅ PASS — the recover-precedence sideways pointer works, correctly branded and repo-scoped.**

**Setup:** no pending snapshot (verified snapshots dir empty), fresh `m28` sandbox.

**Result:** `gitrust --recover` printed:
> *"No interrupted GiTrust pipeline found for this repo. If you're looking for lost commits, try `gitrust "find my lost work"`."*

- Reports **no interrupted pipeline** (correct — nothing pending). ✅
- **Sideways pointer** names the forensic path `gitrust "find my lost work"` verbatim — the two recovery worlds introduce each other. ✅
- **Branding "GiTrust"** — rename landed (no stale "GLit"). ✅
- **Repo-scoped** — *"for this repo"* — reflects the Phase 14 snapshot repo-path scoping (S56); a snapshot from another repo wouldn't be offered here.
- `EXIT=0` — correct (informational success; `--recover` ran and correctly found nothing).

**Repro:** deterministic (with snapshots dir clear).

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
