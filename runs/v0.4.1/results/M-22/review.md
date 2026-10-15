Verdict: PASS-WITH-NOTES
Summary: Revert works with exit 0, but uses its own Y/n question plus plan Enter.

- Prompt "? Revert a7ec361 with a new inverse commit? (Y/n)" is followed by the plan "[Enter] run · [q] cancel". This is a double confirmation and a different key style from other operations (Y/n vs one-key plan).
- Raw git output leaks into the step line: `○  revert    a7ec361[main 4fe1afd] Revert "to be reverted"` / " delete mode 100644 other.txt".
- Behaviour right: one revert commit, other.txt gone, "Reverted a7ec361 (inverse commit added)", exit 0. Not blocked by the pre-commit hook, which matches git.
- The prompt names the SHA but not the commit message, so the user has to know what a7ec361 is.
