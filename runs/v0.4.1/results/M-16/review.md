Verdict: PASS-WITH-NOTES
Summary: Typed confirm and trash backup work; double confirmation and truncated menu text.

- Throw-away path shows a full Destructive/Risks/Recovery/Safety block, then `Type 'a1a7966' to DISCARD commit a1a7966 "feat: the mistake" and all its changes:`. Behaviour is right.
- Success names the backup: "A backup of the discarded changes is in ~/.gitrust/trash/20261015-174209 for 7 days." Exit 0, backup written.
- After the typed confirmation the plan still asks "[Enter] run · [q] cancel", so this is confirmed twice, against the "once" convention. A typed confirm is arguably enough here.
- Menu row 4 says "both go (git keeps them ~90 days)" but uncommitted file changes are not in the reflog (the backup is their only copy). The text is also truncated with "you'll type to con…".
