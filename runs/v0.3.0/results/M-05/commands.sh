# ===== SETUP (M-05) =====
mk_sandbox m05
# ===== COMMAND (M-05) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-05_scratch/work"
$GITRUST "create branch feature-x"; echo x >> app.txt; $GITRUST "checkout $BR"
