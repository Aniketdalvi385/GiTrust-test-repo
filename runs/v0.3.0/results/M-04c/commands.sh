# ===== SETUP (M-04c) =====
mk_sandbox m04c; echo "api client" > api_client.txt; echo "api routes" > api_routes.txt; echo "login page" > login.txt; echo "readme" > README.md
# ===== COMMAND (M-04c) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-04c_scratch/work"
$GITRUST "push all api changes"
