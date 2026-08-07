# ===== SETUP (M-24) =====
mk_sandbox m24; echo wip >> app.txt; git stash push -m "important wip" >/dev/null 2>&1; git stash drop >/dev/null 2>&1
# ===== COMMAND (M-24) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-24_scratch/work"
$GITRUST "find my lost work"
