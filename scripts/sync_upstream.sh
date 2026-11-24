#!/usr/bin/env bash
# ==============================================================================
# Upstream Synchronization Automation for piwd005-Ai
# Pulls latest canonical updates from Primacy-AI-Engineering-Kit while preserving
# all personal skills, MCP server tools, subagent personas, and directives.
# ==============================================================================
set -e

UPSTREAM_URL="https://github.com/primacyinfotechpvtltd/Primacy-AI-Engineering-Kit.git"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=========================================================="
echo "🔄 Checking for Upstream Updates from Senior's Repository"
echo "URL: $UPSTREAM_URL"
echo "=========================================================="

cd "$REPO_DIR"

# Ensure upstream remote exists
if ! git remote | grep -q "^upstream$"; then
    echo "Adding upstream remote..."
    git remote add upstream "$UPSTREAM_URL"
fi

echo "Fetching latest upstream commits..."
git fetch upstream main

# Create a temporary clone/worktree to extract clean canonical files
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

git clone --depth 1 "$UPSTREAM_URL" "$TMP_DIR/upstream"

echo "Syncing canonical upstream directories..."
cp -r "$TMP_DIR/upstream/adapters" "$REPO_DIR/"
cp -r "$TMP_DIR/upstream/docs" "$REPO_DIR/"
cp -r "$TMP_DIR/upstream/evaluations" "$REPO_DIR/"
cp -r "$TMP_DIR/upstream/registry" "$REPO_DIR/"
cp -r "$TMP_DIR/upstream/tests" "$REPO_DIR/"
cp -r "$TMP_DIR/upstream/skills/primacy-engineering" "$REPO_DIR/skills/"
cp "$TMP_DIR/upstream/scripts/build_catalog.py" "$REPO_DIR/scripts/"
cp "$TMP_DIR/upstream/LICENSE" "$REPO_DIR/"
cp "$TMP_DIR/upstream/THIRD_PARTY_NOTICES.md" "$REPO_DIR/"

echo "Running verification test suite..."
python3 -m unittest discover -s tests -v
python3 scripts/build_catalog.py --check

echo ""
echo "=========================================================="
echo "✅ Upstream sync complete! 100% tests passed without regressions."
echo "=========================================================="
