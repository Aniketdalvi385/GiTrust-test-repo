# M-41 · Output piped into head doesn't crash

| | |
|---|---|
| **Part** | 8 · UX |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:43 |
| **Automatic checks** | ❌ failed |

## Checks

- ❌ no panic when the reader closes early — `exit=101 stderr=thread 'main' (2889208) panicked at library/std/src/io/stdio.rs:1165:9:
failed printing to stdout: Broken pipe (os error`

## What a human should judge

(checked by the runner with a closed pipe — see check)

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
