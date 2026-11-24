#!/usr/bin/env bash
# ==============================================================================
# piwd005-Ai Developer Suite - 1-Click Workstation Restore Script
# Restores the entire AI developer suite, skills, plugins, rules, MCP servers,
# and CLI utilities on any fresh machine or developer environment.
# ==============================================================================
set -e

BACKUP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARCHIVE_PATH="$BACKUP_DIR/workstation_full_backup.tar.gz"

echo "=========================================================="
echo "🔄 Restoring piwd005-Ai AI Developer Suite & Workstation"
echo "=========================================================="

# Check if archive exists
if [ ! -f "$ARCHIVE_PATH" ]; then
    echo "❌ Error: Backup archive not found at $ARCHIVE_PATH"
    exit 1
fi

echo "📦 Step 1: Extracting full backup archive to $HOME/odoo_antigravity_sync..."
mkdir -p "$HOME"
tar -xzf "$ARCHIVE_PATH" -C "$HOME"
echo "✓ Extracted to $HOME/odoo_antigravity_sync"

echo ""
echo "🚀 Step 2: Running 1-Click Complete Installer..."
if [ -f "$HOME/odoo_antigravity_sync/install.sh" ]; then
    chmod +x "$HOME/odoo_antigravity_sync/install.sh"
    "$HOME/odoo_antigravity_sync/install.sh"
else
    echo "❌ Error: install.sh not found inside extracted archive!"
    exit 1
fi

echo ""
echo "=========================================================="
echo "🎉 SUCCESS: Complete Workstation & AI Suite Restored!"
echo "=========================================================="
echo "Skills, rules, directives, CLI tools, and plugins are now live on this machine."
echo "CLI tools available: odoo-dev, super-dev"
