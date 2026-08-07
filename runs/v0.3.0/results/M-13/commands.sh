# ===== SETUP (M-13) =====
mk_sandbox m13; git checkout -q "$(git rev-parse HEAD)"; echo x >> app.txt
# ===== COMMAND (M-13) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-13_scratch/work"
$GITRUST "commit this"
