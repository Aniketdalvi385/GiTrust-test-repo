# ===== SETUP (M-03a) =====
mk_sandbox m03a; echo change >> app.txt
# ===== COMMAND (M-03a) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-03a_scratch/work"
$GITRUST "commit this"
