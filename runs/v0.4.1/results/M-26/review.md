Verdict: PASS-WITH-NOTES
Summary: Clean-up deletes only chosen untracked files with backup; wording and raw output nits.

- Menu: "[1] Discard changes to 1 tracked file", "[2] Delete 1 untracked file — never committed, so the trash backup is their only copy", "[3] Both". The counts are clear and it is numbered. Picking 2 touched only junk/, and the tracked edit was untouched.
- Plan has one ⛔ step and "[Enter] run · [q] cancel", with no typed confirmation for deleting unrecoverable files (as the README notes). The trash backup makes it safe, but this is the weakest gate for data that git cannot restore.
- Success: "A backup of the discarded changes is in ~/.gitrust/trash/20261015-174139 for 7 days." This says "discarded changes" although the files were untracked, and "backed up to the trash-net" is jargon.
- Raw git output leaks: `○  delete    untracked filesRemoving junk/`.
