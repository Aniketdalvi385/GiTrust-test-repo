# ===== SETUP (M-04) =====
mk_sandbox m04; echo "login page" > login.txt; echo "login helper" > auth.txt; echo "unrelated" > readme.txt
# ===== COMMAND (M-04) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-04_scratch/work"
$GITRUST "push the login changes"
