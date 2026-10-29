Verdict: PASS-WITH-NOTES
Summary: By hand: one confirmation — the plan and its explanation, then '0059c01' typed in place of Enter; honest Risks; the result names the backup. Copy nits: "This op", and Recovery undersells "find my lost work".

- Plan: "reset  move the branch back to 804a3c6 — changes are discarded ⚠⚠", a warning that the changes are backed up to ~/.gitrust/trash first, then the ⚠⚠ block: "Risks: … GiTrust copies them to ~/.gitrust/trash first (kept 7 days by default)". Then "Type '0059c01' to DISCARD commit 0059c01 "feat: the mistake" and all its changes:" — the only confirmation; nothing asked after it.
- Result: "A backup of the discarded changes is in ~/.gitrust/trash/20261029-105037 for 7 days." Tree clean, commit gone, exit 0.
- Copy: "Safety: This op requires…" is internal wording; "Recovery: … you can recover the commit if you remember the SHA" — `gitrust "find my lost work"` finds it without the SHA.
- A first attempt picked "Undo, keep the changes staged" (no typed confirmation, no backup — right for that option) and so failed this test's checks; this record is the re-run with the throw-away option.
- v0.4.1 notes: F9 and F17 fixed — no separate type-to-confirm before the plan, and Risks no longer says the uncommitted work "is gone".
