# M-30 · Not a repo

| | |
|---|---|
| **LLM** | no |
| **Flagship** | — |
| **Result** | ❌ FAIL (exit 0 — 7th/final exit-code confirmation) |
| **Run date** | 2026-08-05 |

## What this proves

Friendly not-a-repo, nonzero exit.

## Procedure

**Steps:**
```bash
cd /tmp && $GITRUST "status"; echo $?
```

**Expect:** friendly not-a-repo message, no stack trace, nonzero exit.

## Result

**❌ FAIL — friendly message ✅, but exits 0 outside a git repo. The most fundamental confirmation of the systemic exit-code bug.**

**Run:** `gitrust "status"` inside `/tmp/not_a_repo` (a non-git directory).

- **✅ Friendly message, no panic:** *"✗ Not inside a git repository. Run 'gitrust "initialize a repository"' or 'git init' first."* — human-readable, names two fixes, no Rust backtrace.
- **❌ Exit code 0 — must be nonzero.** `EXIT=0`. The defining assertion is a **nonzero** exit, and it failed. Running the tool **outside any git repository at all** — the most basic error case — returns success. A script doing `gitrust "status" && …` proceeds as if in a valid repo.

**7th and final confirmation of the systemic exit-code bug.** Every non-success terminal state observed in this run returned 0:
| Test | Non-success case | Exit |
|---|---|---|
| M-08 | paused rebase (conflict) | 0 |
| M-17 | `--yes` refused undo | 0 |
| M-21 | hook-blocked commit | 0 |
| M-22 | failed revert (dirty tree, status 128) | 0 |
| M-27 | fail-closed clean refusal | 0 |
| M-29 | LLM-connection failure | 0 |
| **M-30** | **not-a-repo** | **0** |

There is now **zero doubt**: GiTrust returns exit 0 on **every** failure/refusal/block/error path. For a CLI positioned as scriptable and safety-focused, this is arguably the single highest-priority fix (peer to the reset phantom-op). The `✗` glyph is present in the *message* on many of these — the process exit code simply doesn't follow it. Likely a single top-level seam: error/refusal results are rendered and then `Ok(())` is returned instead of a nonzero exit.

**Repro:** deterministic.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
