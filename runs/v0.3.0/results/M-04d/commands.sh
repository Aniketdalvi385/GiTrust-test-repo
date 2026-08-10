# ===== SETUP (M-04d) =====
mk_sandbox m04d; echo "users schema" > schema.sql; echo "orders schema" > migrations.sql; echo "api client" > api_client.txt; echo "readme" > README.md
# ===== COMMAND (M-04d) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-04d_scratch/work"
$GITRUST "push all schema changes"
