# GiTrust v0.2.0 — Manual Acceptance Run

Human-eyes acceptance run for the GiTrust `gitrust 0.2.0` release binary. Each row links a
labeled folder with that test's description, the exact commands, the captured output, and — for
the flagship demos — a screen recording. This is the experience-level complement to the 192
automated `cargo test` cases.

- **This run's report:** [REPORT.md](REPORT.md) — verdicts, root-cause clusters, keep-list
- **Full suite (reference):** [../../MANUAL_TEST_SUITE.md](../../MANUAL_TEST_SUITE.md)
- **How to run locally:** [../../harness.sh](../../harness.sh) — source it once per terminal, then follow each folder's README.

Tests ran against a **local throwaway bare remote** per case (under the repo-root `sandboxes/`, git-ignored — never pushed).
Only the records in `results/` and `evidence/` are committed.

## Environment

| Field | Value |
|---|---|
| Date | 2026-07-31 → 2026-08-05 |
| OS / arch | macOS (Darwin) / arm64 |
| git version | 2.39.5 (Apple Git-154) |
| `gitrust --version` | 0.2.0 |
| Ollama model | qwen2.5:3b (Homebrew `brew services`) |

## Result: 19 ✅ · 4 ⚠️ · 8 ❌

| ID | Title | LLM | Rec | Result |
|---|---|---|---|---|
| [M-00](results/M-00/) | Build, version, setup | yes |  | ✅ PASS |
| [M-01](results/M-01/) | Fast-path status (Ollama off) | no |  | ✅ PASS |
| [M-02](results/M-02/) | LLM-path classification | yes |  | ✅ PASS |
| [M-03](results/M-03/) | Commit with editable message | yes |  | ✅ PASS |
| [M-04](results/M-04/) | Scoped feature pipeline ★ | yes | 🎥 | ❌ FAIL |
| [M-05](results/M-05/) | Branch create + dirty-switch block | no |  | ❌ FAIL |
| [M-06](results/M-06/) | Diverged push → rebase → clean ★ | yes | 🎥 | ✅ PASS |
| [M-07](results/M-07/) | Diverged → merge path | yes |  | ✅ PASS |
| [M-08](results/M-08/) | Conflicting rebase → calm pause → continue ★ | partial | 🎥 | ⚠️ PASS (3 defects) |
| [M-09](results/M-09/) | Abort restores exactly | no |  | ⚠️ PASS (defects) |
| [M-10](results/M-10/) | Sync with main via origin/HEAD | yes |  | ❌ FAIL |
| [M-11](results/M-11/) | Mid-rebase never says checkout a branch | yes |  | ✅ PASS |
| [M-12](results/M-12/) | Merge-aware commit: two parents | yes |  | ✅ PASS |
| [M-13](results/M-13/) | Detached write → rescue | yes |  | ⚠️ PASS (partial) |
| [M-14](results/M-14/) | Stranded-commit guard ★ | no | 🎥 | ✅ PASS |
| [M-15](results/M-15/) | Undo gate: four options, names the commit | no |  | ✅ PASS |
| [M-16](results/M-16/) | Undo → discard: TypeToConfirm + trash-net | no |  | ❌ FAIL (CRITICAL) |
| [M-17](results/M-17/) | --yes cannot undo | no |  | ❌ FAIL |
| [M-18](results/M-18/) | Multi-count undo halts with guidance | yes |  | ✅ PASS |
| [M-19](results/M-19/) | Squash last 3: tree-identical | yes |  | ❌ FAIL |
| [M-20](results/M-20/) | Amend-on-pushed: escalation + lease ★ | yes | 🎥 | ❌ FAIL |
| [M-21](results/M-21/) | Failing pre-commit blocks (via system git) | yes |  | ⚠️ PASS (exit-0 defect) |
| [M-22](results/M-22/) | Revert parity: succeeds despite the same hook | no |  | ✅ PASS |
| [M-23](results/M-23/) | Deleted branch → find my lost work ★★ | no | 🎥 | ✅ PASS |
| [M-24](results/M-24/) | Dropped stash surfaces | no |  | ✅ PASS |
| [M-25](results/M-25/) | Empty-scan honesty | no |  | ✅ PASS |
| [M-26](results/M-26/) | Clean-up gate + trash backup, nested dirs | no |  | ✅ PASS |
| [M-27](results/M-27/) | Fail-closed trash-net | no |  | ✅ PASS (exit-0 defect) |
| [M-28](results/M-28/) | Recover precedence: sideways pointer | no |  | ✅ PASS |
| [M-29](results/M-29/) | Ollama down: graceful degrade | — |  | ✅ PASS |
| [M-30](results/M-30/) | Not a repo | no |  | ❌ FAIL |

🎥 = screen recording in [evidence/](evidence/) · ★ / ★★ = flagship demo

## Running-order notes (for reproducing this run)

- **Run M-27 LAST** (or `chmod 755 ~/.gitrust/trash` immediately after) — it makes the trash dir
  unwritable; forget the cleanup and every later trash test (M-16, M-24, M-26) fails-closed and
  looks like a product bug.
- **Stopping Ollama on this machine** requires `brew services stop ollama` (it runs as a Homebrew
  launchd service; `pkill` is auto-revived). Restart with `brew services start ollama`. Relevant to
  M-01 and M-29.
- Clear `~/.gitrust/snapshots/*.json` between conflict/undo tests — several ops leave a stale
  snapshot that triggers a spurious "interrupted pipeline" warning (a logged v0.2.0 defect).
