# GiTrust v0.2 — Manual Acceptance Test Report

**Binary:** `gitrust 0.2.0` · **Date:** 2026-07-31 → 2026-08-05 · **Platform:** macOS (Darwin) / arm64 · **git:** 2.39.5 · **Ollama model:** qwen2.5:3b (via Homebrew `brew services`)

All 31 tests (M-00 … M-30) executed one-by-one against the release binary in throwaway local sandboxes. Per-test evidence (commands, output, notes, and recordings for the flagship demos) is in [`results/M-NN/`](results/). This is the experience-level complement to the 192 automated `cargo test` cases.

## Result summary

| Verdict | Count | Tests |
|---|---|---|
| ✅ PASS | 19 | M-00, M-01, M-02, M-03, M-06, M-07, M-11, M-12, M-14, M-15, M-18, M-22, M-23, M-24, M-25, M-26, M-27, M-28, M-29 |
| ⚠️ PASS with defects | 4 | M-08, M-09, M-13, M-21 |
| ❌ FAIL | 8 | M-04, M-05, M-10, M-16, M-17, M-19, M-20, M-30 |

**Headline:** the tool's **reason to exist — forensic recovery — is excellent** (M-23 ★★, M-24, M-25, M-26, M-27, M-28 all pass, several flawless). The failures cluster into **three well-isolated root causes**, not scattered breakage.

## Full results table

| ID | Title | LLM | Flag | Result |
|---|---|---|---|---|
| M-00 | Build, version, setup | yes | | ✅ PASS |
| M-01 | Fast-path status (Ollama off) | no | | ✅ PASS |
| M-02 | LLM-path classification | yes | | ✅ PASS |
| M-03 | Commit with editable message | yes | | ✅ PASS |
| M-04 | Scoped feature pipeline | yes | ★ | ❌ FAIL |
| M-05 | Branch create + dirty-switch block | no | | ❌ FAIL |
| M-06 | Diverged push → rebase → clean | yes | ★ | ✅ PASS |
| M-07 | Diverged → merge path | yes | | ✅ PASS |
| M-08 | Conflicting rebase → calm pause → continue | partial | ★ | ⚠️ PASS (3 defects) |
| M-09 | Abort restores exactly | no | | ⚠️ PASS (defects) |
| M-10 | Sync with main via origin/HEAD | yes | | ❌ FAIL |
| M-11 | Mid-rebase never says checkout a branch | yes | | ✅ PASS |
| M-12 | Merge-aware commit: two parents | yes | | ✅ PASS |
| M-13 | Detached write → rescue | yes | | ⚠️ PASS (commit dropped) |
| M-14 | Stranded-commit guard | no | ★ | ✅ PASS |
| M-15 | Undo gate: four options, names the commit | no | | ✅ PASS |
| M-16 | Undo → discard: TypeToConfirm + trash-net | no | | ❌ FAIL 🔴 CRITICAL |
| M-17 | --yes cannot undo | no | | ❌ FAIL |
| M-18 | Multi-count undo halts with guidance | yes | | ✅ PASS |
| M-19 | Squash last 3: tree-identical | yes | | ❌ FAIL |
| M-20 | Amend-on-pushed: escalation + lease | yes | ★ | ❌ FAIL |
| M-21 | Failing pre-commit blocks (via system git) | yes | | ⚠️ PASS (exit-0) |
| M-22 | Revert parity: succeeds despite the same hook | no | | ✅ PASS |
| M-23 | Deleted branch → find my lost work | no | ★★ | ✅ PASS (flawless) |
| M-24 | Dropped stash surfaces | no | | ✅ PASS |
| M-25 | Empty-scan honesty | no | | ✅ PASS |
| M-26 | Clean-up gate + trash backup, nested dirs | no | | ✅ PASS |
| M-27 | Fail-closed trash-net | no | | ✅ PASS (exit-0) |
| M-28 | Recover precedence: sideways pointer | no | | ✅ PASS |
| M-29 | Ollama down: graceful degrade | — | | ✅ PASS |
| M-30 | Not a repo | no | | ❌ FAIL |

## The three root-cause clusters (fix targets)

### 🔴 1. Systemic exit-code bug — **every** non-success path returns exit 0
Confirmed **7 independent times**: M-08 (paused rebase), M-17 (`--yes` refused undo), M-21 (hook-blocked commit), M-22 (failed revert / git status 128), M-27 (fail-closed refusal), M-29 (LLM connection failure), **M-30 (not a git repo)**. The `✗` glyph appears in the *message*, but the process exit code is `0`. **Impact:** the CLI is unsafe to script — `gitrust … && next` proceeds after failures/refusals/blocks, even when run outside a repo entirely. **Likely fix:** one top-level seam renders the error then returns `Ok(())` instead of a nonzero code. Highest-priority, lowest-effort fix.

### 🔴 2. Reset execution path is a phantom op — reports success, does nothing
M-16 (`reset --hard` via undo→discard) and M-19 (`reset --soft` via squash) **both** print `✓ Done`/`reset (…)` while **HEAD never moves** and, for M-16, the promised trash backup is **never written** (dir doesn't exist) — a destructive op that lies about a safety net that isn't there. **Isolated by M-26/M-27:** the trash-net module itself is *sound* (M-26 writes a real byte-identical nested backup; M-27 fail-closes correctly) — so the bug is specifically the **reset executor emitting success copy from step metadata without performing/verifying the git mutation**. Fix `Git2Operations::reset` (Hard + Soft). Critical because M-16 both (a) claims a false backup and (b) no-ops the discard.

### 3. Argument/target extraction from the user's phrase (intent routing)
Requests that carry a **target/scope/argument** are dropped or misrouted: M-04 (scope "the login changes" → committed all files incl. unrelated), M-05 (`create branch X` / `checkout X` → branch-list / "no target branch"), M-10 (`sync with main` → plain status, no rebase), M-19 ("squash the last 3" → single-commit soft reset), M-20 (amend intent flaky + clarification loop never converges). **Boundary proven:** "recognize-but-don't-act" works (M-18 correctly declined a 3-commit undo; M-12 committed a merge from on-disk `MERGE_HEAD`); "recognize-and-act-on-extracted-target" is the weak spot. Fix the argument-slot capture in the phrase table and the LLM intent classifier.

## Secondary defects (lower priority)
- **Snapshot lifecycle** (M-08, M-09, M-19, M-21): pause/continue/abort/blocked-commit leave a `~/.gitrust/snapshots/*.json` behind → spurious "interrupted pipeline — run --recover" warning nags on later commands (even read-only `status`), and points at `--recover` which could undo completed work.
- **Conflicted-file count "0"** (M-08, M-09): the calm-pause message says "conflicts in 0 file(s)" and doesn't name the file (should be 1, `app.txt`).
- **Dropped continuation after redirect** (M-13): detached-HEAD rescue creates the branch but doesn't complete the user's original `commit`.
- **Copy bugs:** M-17 undo refusal cites "rebase vs merge strategy" (wrong op); M-12 keeps `# Conflicts:` comment lines in the commit message; M-16 TypeToConfirm says "type the branch name" but asks for the commit oid.
- **Marker glyph** (M-02): binary prints `@` for LLM path; suite text said `◉` (cosmetic).
- **Redundant warning** (M-06, M-07): "consider pulling first" shown inside a plan that already rebases/merges.
- **Long-subject pass-through** (M-03): 84-char commit subject warned but committed anyway (no re-prompt).

## What works well (keep)
- **Forensic recovery subsystem** — the two-source design is real and verified: Source A/reflog recovers deleted branches (M-23 ★★, flawless — rescue at exact oid, HEAD untouched), Source B/odb-scan recovers dropped stashes (M-24, byte-perfect, `[stash]`-tagged). Empty-scan honesty (M-25) and recover-precedence pointer (M-28) both correct.
- **Trash-net (clean path)** — real byte-identical nested-dir backup (M-26), correct fail-closed refusal (M-27), Windows-safe timestamps.
- **Divergence reconcile** — rebase (M-06 ★) and merge (M-07) both clean, ChoiceGate with plain-English consequences.
- **Safety guards** — stranded-commit guard (M-14 ★), merge-aware two-parent commit (M-12), hook enforcement + system-git routing (M-21), S12 regression dead (M-11).
- **Graceful degrade** — Ollama-down falls back to a usable manual mode (M-29), fast path stays instant (M-01).

## Flagship recordings
M-04 (fail), M-06 (pass), M-08 (pass w/ defects), M-14 (pass), M-20 (fail), M-23 ★★ (flawless) — see `evidence/`.
