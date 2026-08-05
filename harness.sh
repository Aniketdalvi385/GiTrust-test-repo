# Source this once per terminal session:  source harness.sh   (from the repo root)
# Provides: $GITRUST, $TESTROOT, $REPO_ROOT, mk_sandbox, mk_teammate, and (after mk_sandbox) $BR.

# Repo root = wherever this script lives (location-independent; survives moving the repo).
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"

# Point $GITRUST at the release binary for the version under test.
# Rebuild (`cargo build --release` in gitrust/) before each new version's run, then confirm
# `$GITRUST --version` matches the run folder you record into (runs/vX.Y.Z).
GITRUST=/Users/aniket.dalvi/Desktop/personal/Glit/gitrust/target/release/gitrust
TESTROOT="$REPO_ROOT/sandboxes"

mk_sandbox() {                                  # fresh bare remote + working clone
  local name=$1
  rm -rf "$TESTROOT/$name" && mkdir -p "$TESTROOT/$name" && cd "$TESTROOT/$name" || return 1
  git init --bare remote.git -q
  git clone -q remote.git work 2>/dev/null; cd work || return 1
  git config user.email you@test.com && git config user.name you
  echo "base" > app.txt && git add . && git commit -qm "base"
  BR=$(git symbolic-ref --short HEAD)           # 'main' on this machine
  git push -q -u origin "$BR"
  echo "sandbox '$name' ready — BR=$BR, cwd=$(pwd)"
}

mk_teammate() {                                 # second clone that pushes a commit you never pull
  ( cd "$TESTROOT/$1" && git clone -q remote.git teammate && cd teammate \
    && git config user.email t@test.com && git config user.name teammate \
    && echo "teammate hotfix" >> notes.txt && git add . && git commit -qm "teammate: hotfix" && git push -q )
  echo "teammate pushed a commit to $1's remote"
}

echo "harness loaded — GITRUST=$GITRUST"
echo "REPO_ROOT=$REPO_ROOT"
echo "TESTROOT=$TESTROOT"
