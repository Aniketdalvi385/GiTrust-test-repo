Verdict: FAIL
Summary: Rust panic (exit 101) when piped output reader closes early.

- Runner check failed: "exit=101 stderr=thread 'main' panicked at library/std/src/io/stdio.rs:1165:9: failed printing to stdout: Broken pipe". This is a panic from println! on EPIPE, e.g. `gitrust history | head`, violating the no-panic convention.
- Screens show the normal (unclosed) run fine (exit 0), so the defect is only on early reader close. Fix: reset SIGPIPE to default at startup or use writeln! and ignore BrokenPipe errors.
- Pipe-mode first line is "+  Show history · 2.1s" (ASCII marker for the model); also the "--yes" run took 2.1s, fine.
