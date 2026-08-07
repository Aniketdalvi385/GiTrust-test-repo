# ===== SETUP (M-10) =====
mk_sandbox m10; git remote set-head origin --auto; git checkout -qb feature; mk_teammate m10; git fetch -q
# ===== COMMAND (M-10) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-10_scratch/work"
$GITRUST "sync with main"
