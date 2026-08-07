# ===== SETUP (M-17) =====
mk_sandbox m17; echo v2 >> app.txt && git commit -qam "to undo"; PRE=$(git rev-parse HEAD); echo "PRE=$PRE" > "$SBX/PRE.txt"
# ===== COMMAND (M-17) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-17_scratch/work"
$GITRUST --yes "undo"; echo "EXIT=$?"
