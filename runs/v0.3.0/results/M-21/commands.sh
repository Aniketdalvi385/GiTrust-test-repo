# ===== SETUP (M-21) =====
mk_sandbox m21; printf "#!/bin/sh\necho \"LINT FAILED\"; exit 1\n" > .git/hooks/pre-commit; chmod +x .git/hooks/pre-commit; echo x >> app.txt; git rev-list --count HEAD > "$SBX/COUNT.txt"
# ===== COMMAND (M-21) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-21_scratch/work"
$GITRUST "commit this"; echo "EXIT=$?"
