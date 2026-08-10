# ===== SETUP (M-04b) =====
mk_sandbox m04b; echo "readme docs" > README.md; echo "guide docs" > docs/guide.md 2>/dev/null || (mkdir -p docs && echo "guide docs" > docs/guide.md); echo "login page" > login.txt; echo "schema def" > schema.sql
# ===== COMMAND (M-04b) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-04b_scratch/work"
$GITRUST "push all docs changes"
