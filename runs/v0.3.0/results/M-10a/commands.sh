# ===== SETUP (M-10a) =====
mk_sandbox m10a; git remote set-head origin --auto; mk_teammate m10a; git fetch -q; git checkout -qb feature
# ===== COMMAND (M-10a) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-10a_scratch/work"
$GITRUST "sync with main"
