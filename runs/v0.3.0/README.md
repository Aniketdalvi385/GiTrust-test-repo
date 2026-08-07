# GiTrust v0.3.0 — acceptance run

| Field | Value |
|---|---|
| Date | 2026-08-07 |
| OS / arch | Darwin arm64 |
| git | 2.39.5 |
| `gitrust --version` | 0.3.0 |
| Ollama model | qwen2.5:3b |

**Verdicts:** ✅ 28 PASS · ⚠️ 2 PASS-with-defects · ❌ 0 FAIL · ⛔ 0 BLOCKED · ⏭️ 1 SKIP

| ID | Title | LLM | Result |
|---|---|---|---|
| [M-00](results/M-00/) | Build, version, setup | yes | ✅ PASS |
| [M-01](results/M-01/) | Fast-path status (Ollama OFF) | no | ✅ PASS |
| [M-02](results/M-02/) | LLM-path classification | yes | ✅ PASS |
| [M-03](results/M-03/) | Commit with editable message | yes | ✅ PASS |
| [M-04](results/M-04/) | Scoped feature pipeline (flagship) | yes | ✅ PASS |
| [M-05](results/M-05/) | Branch create + dirty switch block | no | ✅ PASS |
| [M-06](results/M-06/) | Diverged push -> rebase -> clean (flagship) | yes | ✅ PASS |
| [M-07](results/M-07/) | Diverged -> merge path | yes | ✅ PASS |
| [M-08](results/M-08/) | Conflicting rebase -> calm pause -> continue (flagship) | partial | ✅ PASS |
| [M-09](results/M-09/) | Abort restores exactly | no | ✅ PASS |
| [M-10](results/M-10/) | Sync with main via origin/HEAD | yes | ✅ PASS |
| [M-11](results/M-11/) | Mid-rebase never says checkout a branch | yes | ✅ PASS |
| [M-12](results/M-12/) | Merge-aware commit: two parents | yes | ✅ PASS |
| [M-13](results/M-13/) | Detached write -> rescue | yes | ⚠️ PASS (with defects) |
| [M-14](results/M-14/) | Stranded-commit guard (flagship) | no | ✅ PASS |
| [M-15](results/M-15/) | Undo gate: four options, names the commit | no | ✅ PASS |
| [M-16](results/M-16/) | Undo -> discard: TypeToConfirm + trash-net | no | ✅ PASS |
| [M-17](results/M-17/) | --yes cannot undo | no | ✅ PASS |
| [M-18](results/M-18/) | Multi-count undo halts with guidance | yes | ✅ PASS |
| [M-19](results/M-19/) | Squash last 3: tree-identical | yes | ✅ PASS |
| [M-20](results/M-20/) | Amend-on-pushed: escalation + lease (flagship) | yes | ✅ PASS |
| [M-21](results/M-21/) | Failing pre-commit blocks (via system git) | yes | ⚠️ PASS (with defects) |
| [M-22](results/M-22/) | Revert parity: succeeds despite the same hook | no | ✅ PASS |
| [M-23](results/M-23/) | Deleted branch -> find my lost work (flagship) | no | ✅ PASS (flawless) |
| [M-24](results/M-24/) | Dropped stash surfaces | no | ✅ PASS |
| [M-25](results/M-25/) | Empty-scan honesty | no | ✅ PASS |
| [M-26](results/M-26/) | Clean-up gate + trash backup, nested dirs | no | ✅ PASS |
| [M-27](results/M-27/) | Fail-closed trash-net | no | ✅ PASS |
| [M-28](results/M-28/) | Recover precedence: sideways pointer | no | ✅ PASS |
| [M-29](results/M-29/) | Ollama down: graceful degrade | dash | ⏭️ SKIP (not exercised — Ollama was up) |
| [M-30](results/M-30/) | Not a repo | no | ✅ PASS |
