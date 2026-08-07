# ===== SETUP (M-15) =====
mk_sandbox m15; echo v2 >> app.txt && git commit -qam "feat: the mistake"
# ===== COMMAND (M-15) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-15_scratch/work"
$GITRUST "undo"
