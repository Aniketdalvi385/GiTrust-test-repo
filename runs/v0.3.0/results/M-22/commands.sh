# ===== SETUP (M-22) =====
mk_sandbox m22; printf "#!/bin/sh\necho \"LINT FAILED\"; exit 1\n" > .git/hooks/pre-commit; chmod +x .git/hooks/pre-commit; echo v2 >> app.txt && git commit -qam "to revert" --no-verify
# ===== COMMAND (M-22) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-22_scratch/work"
$GITRUST "revert last commit"
