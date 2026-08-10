# GiTrust v0.3.0 — acceptance run

| Field | Value |
|---|---|
| Date | 2026-08-10 |
| OS / arch | Darwin arm64 |
| git | 2.39.5 |
| `gitrust --version` | 0.3.0 |
| Ollama model | qwen2.5:3b |

**Verdicts:** ✅ 35 PASS · ⚠️ 2 PASS-with-defects · ❌ 5 FAIL · ⛔ 0 BLOCKED · ⏭️ 0 SKIP

| ID | Title | LLM | Result |
|---|---|---|---|
| [M-00](results/M-00/) | Build, version, setup | yes | ✅ PASS |
| [M-01](results/M-01/) | Fast-path status (Ollama OFF) | no | ✅ PASS |
| [M-02](results/M-02/) | LLM-path classification | yes | ✅ PASS |
| [M-03a](results/M-03a/) | Commit with editable message — "commit this" | yes | ✅ PASS |
| [M-03b](results/M-03b/) | Commit with editable message — "save my changes" | yes | ✅ PASS |
| [M-03c](results/M-03c/) | Commit with editable message — "commit everything" | yes | ✅ PASS |
| [M-04a](results/M-04a/) | Scoped feature pipeline — login scope | partial | ⚠️ PASS (with defects) |
| [M-04b](results/M-04b/) | Scoped feature pipeline — docs scope | yes | ❌ FAIL |
| [M-04c](results/M-04c/) | Scoped feature pipeline — api scope | partial | ⚠️ PASS (with defects) |
| [M-04d](results/M-04d/) | Scoped feature pipeline — schema scope | yes | ❌ FAIL |
| [M-05](results/M-05/) | Branch create + dirty switch block | no | ✅ PASS |
| [M-06](results/M-06/) | Diverged push -> rebase -> clean (flagship) | yes | ✅ PASS |
| [M-07](results/M-07/) | Diverged -> merge path | yes | ✅ PASS |
| [M-08](results/M-08/) | Conflicting rebase -> calm pause -> continue (flagship) | partial | ✅ PASS |
| [M-09](results/M-09/) | Abort restores exactly | no | ✅ PASS |
| [M-10a](results/M-10a/) | Sync feature with a target branch — "sync with main" | no | ✅ PASS |
| [M-10b](results/M-10b/) | Sync feature with a target branch — "update feature from main" | no | ✅ PASS |
| [M-10c](results/M-10c/) | Sync feature with a target branch — "pull main into feature" | yes | ❌ FAIL |
| [M-11](results/M-11/) | Mid-rebase never says checkout a branch | yes | ✅ PASS |
| [M-12](results/M-12/) | Merge-aware commit: two parents | yes | ✅ PASS |
| [M-13](results/M-13/) | Detached write -> rescue | yes | ✅ PASS |
| [M-14](results/M-14/) | Stranded-commit guard (flagship) | no | ✅ PASS |
| [M-15](results/M-15/) | Undo gate: four options, names the commit | no | ✅ PASS |
| [M-16](results/M-16/) | Undo -> discard: TypeToConfirm + trash-net | no | ✅ PASS |
| [M-17](results/M-17/) | --yes cannot undo | no | ✅ PASS |
| [M-18](results/M-18/) | Multi-count undo halts with guidance | yes | ✅ PASS |
| [M-19a](results/M-19a/) | Squash last 3 — digit "last 3 commits" | yes | ✅ PASS |
| [M-19b](results/M-19b/) | Squash last 3 — word "last three commits" | yes | ❌ FAIL |
| [M-19c](results/M-19c/) | Squash last 3 — verb "combine the last 3" | yes | ✅ PASS |
| [M-20a](results/M-20a/) | Amend-on-pushed — "fix the last commit message to …" | yes | ✅ PASS |
| [M-20b](results/M-20b/) | Amend-on-pushed — "reword the last commit to …" | yes | ❌ FAIL |
| [M-20c](results/M-20c/) | Amend-on-pushed — "change my last commit message to …" | yes | ✅ PASS |
| [M-21](results/M-21/) | Failing pre-commit blocks (via system git) | yes | ✅ PASS |
| [M-22](results/M-22/) | Revert parity: succeeds despite the same hook | no | ✅ PASS |
| [M-23](results/M-23/) | Deleted branch -> find my lost work (flagship) | no | ✅ PASS (flawless) |
| [M-24](results/M-24/) | Dropped stash surfaces | no | ✅ PASS |
| [M-25](results/M-25/) | Empty-scan honesty | no | ✅ PASS |
| [M-26](results/M-26/) | Clean-up gate + trash backup, nested dirs | no | ✅ PASS |
| [M-27](results/M-27/) | Fail-closed trash-net | no | ✅ PASS |
| [M-28](results/M-28/) | Recover precedence: sideways pointer | no | ✅ PASS |
| [M-29](results/M-29/) | Ollama down: graceful degrade | dash | ✅ PASS |
| [M-30](results/M-30/) | Not a repo | no | ✅ PASS |
