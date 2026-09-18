#!/usr/bin/env bash
# sync-shared.sh — copy the single-source `shared/` folder into each plugin as `<plugin>/shared/`,
# so `${CLAUDE_PLUGIN_ROOT}/shared/...` resolves inside every installed plugin.
# Run after editing anything under shared/. `--check` only reports drift (exit 1 when out of sync).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/shared"
PLUGINS=("$ROOT/plugins/oracle-packs" "$ROOT/plugins/oracle-packs-web")
MODE="${1:-sync}"

rc=0
for p in "${PLUGINS[@]}"; do
  dst="$p/shared"
  if [ "$MODE" = "--check" ]; then
    # The same exclusions as the sync below, or --check reports drift on the very
    # thing the sync deliberately leaves behind (shared/tools/tests/).
    if [ ! -d "$dst" ] || ! diff -rq --exclude='__pycache__' --exclude='.DS_Store' \
         --exclude='tests' "$SRC" "$dst" >/dev/null; then
      echo "DRIFT: $dst differs from shared/ (run tools/sync-shared.sh)"; rc=1
    else
      echo "OK: $dst"
    fi
  else
    mkdir -p "$dst"
    rsync -a --delete --exclude='__pycache__' --exclude='.DS_Store' --exclude='tests/' "$SRC/" "$dst/"
    echo "synced: $dst"
  fi
done
exit $rc
