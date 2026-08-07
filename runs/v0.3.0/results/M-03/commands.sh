# ===== SETUP (M-03) =====
mk_sandbox m03; echo change >> app.txt
# ===== COMMAND (M-03) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-03_scratch/work"
$GITRUST "commit this"
