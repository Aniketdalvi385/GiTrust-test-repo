# ===== SETUP (M-04a) =====
mk_sandbox m04a; echo "login page" > login.txt; echo "login helper" > auth.txt; echo "unrelated" > readme.txt; echo "api thing" > api_client.txt
# ===== COMMAND (M-04a) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-04a_scratch/work"
$GITRUST "push the login changes"
