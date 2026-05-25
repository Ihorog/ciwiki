#!/bin/bash
# Merge multiple PRs sequentially
set -e

REPO="Ihorog/ciwiki"
PRS=(205 204 203 202 199 198 197)

for pr in "${PRS[@]}"; do
  echo "[*] Merging PR #$pr..."
  gh pr merge "$pr" \
    --repo "$REPO" \
    --squash \
    --auto || echo "[!] PR #$pr merge failed or already merged"
  sleep 2
done

echo "[✓] All PRs processed"
