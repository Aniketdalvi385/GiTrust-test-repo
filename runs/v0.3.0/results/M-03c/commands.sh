# ===== SETUP (M-03c) =====
mk_sandbox m03c; echo change >> app.txt
# ===== COMMAND (M-03c) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-03c_scratch/work"
$GITRUST "commit everything"
