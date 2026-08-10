# ===== SETUP (M-03b) =====
mk_sandbox m03b; echo change >> app.txt
# ===== COMMAND (M-03b) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-03b_scratch/work"
$GITRUST "save my changes"
