#!/usr/bin/env bash
# ==============================================================================
# Private-Ai AI Developer Suite - 1-Click Complete Installer
# Installs all skills, rules, odoo-dev plugin, MCP tools, and CLI to any machine
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================================="
echo "🚀 Installing Private-Ai Developer Suite & AI Engineering Kit"
echo "=========================================================="

# 1. Check Python 3
if ! command -v python3 &>/dev/null; then
    echo "❌ Error: python3 is not installed. Please install python3 first."
    exit 1
fi
echo "✓ Python 3 detected: $(python3 --version)"

# 2. Install Required Python Libraries
echo ""
echo "📦 Step 1: Installing Python Libraries (Odoo RPC, MCP, Document Readers, Linters)..."
python3 -m pip install --user --break-system-packages \
    pylint-odoo \
    odoorpc \
    mcp \
    pandas \
    "openpyxl>=3.1.5" \
    python-docx \
    pypdf \
    Pillow \
    pytest \
    coverage \
    playwright \
    psycopg2-binary 2>/dev/null || \
python3 -m pip install --user \
    pylint-odoo \
    odoorpc \
    mcp \
    pandas \
    "openpyxl>=3.1.5" \
    python-docx \
    pypdf \
    Pillow \
    pytest \
    coverage \
    playwright \
    psycopg2-binary

echo "✓ Python libraries installed successfully."

# Install Playwright browser binary
echo "🌐 Installing Playwright Chromium browser binary for visual verification..."
python3 -m playwright install chromium 2>/dev/null || true
echo "✓ Chromium browser ready."

# 3. Create Target Directories
echo ""
echo "📁 Step 2: Preparing Target Directories..."
mkdir -p "$HOME/.gemini/config/skills"
mkdir -p "$HOME/.gemini/config/plugins/odoo-dev"
mkdir -p "$HOME/.gemini/config/plugins/super-dev"
mkdir -p "$HOME/.gemini/antigravity/mcp/odoo-dev"
mkdir -p "$HOME/.gemini/antigravity/mcp/odoo-dev_odoo-dev"
mkdir -p "$HOME/.local/bin"

# 4. Copy Skills (Global)
echo "📂 Step 3: Installing All Global Skills (Universal Suite + Primacy Engineering Kit)..."
cp -r "$SCRIPT_DIR/skills/"* "$HOME/.gemini/config/skills/"
echo "✓ Skills installed in ~/.gemini/config/skills/"

# 5. Copy Plugins (odoo-dev and super-dev)
echo "🔌 Step 4: Installing Plugins & MCP Servers..."
cp -r "$SCRIPT_DIR/plugins/odoo-dev/"* "$HOME/.gemini/config/plugins/odoo-dev/"
chmod +x "$HOME/.gemini/config/plugins/odoo-dev/mcp_server.py"
cp -r "$SCRIPT_DIR/plugins/super-dev/"* "$HOME/.gemini/config/plugins/super-dev/"
echo "✓ Plugins installed in ~/.gemini/config/plugins/"

# 6. Configure Global MCP Server
echo "⚙️ Step 5: Registering MCP Server in ~/.gemini/config/mcp_config.json..."
python3 -c "
import json, os

cfg_path = os.path.expanduser('~/.gemini/config/mcp_config.json')
os.makedirs(os.path.dirname(cfg_path), exist_ok=True)
try:
    with open(cfg_path, 'r') as f:
        data = json.load(f)
except Exception:
    data = {}
servers = data.setdefault('mcpServers', {})
servers['odoo-dev'] = {
    'command': '/usr/bin/python3',
    'args': [os.path.expanduser('~/.gemini/config/plugins/odoo-dev/mcp_server.py')]
}
with open(cfg_path, 'w') as f:
    json.dump(data, f, indent=2)
"
echo "✓ Global MCP server registered."

# 7. Install CLI tools
echo "🛠 Step 6: Installing super-dev & odoo-dev CLI Utilities to ~/.local/bin/..."
cp "$SCRIPT_DIR/bin/super-dev" "$HOME/.local/bin/super-dev"
chmod +x "$HOME/.local/bin/super-dev"
cp "$SCRIPT_DIR/bin/odoo-dev" "$HOME/.local/bin/odoo-dev"
chmod +x "$HOME/.local/bin/odoo-dev"

# Ensure ~/.local/bin is in PATH in ~/.bashrc and ~/.zshrc if exists
for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
    if [ -f "$rc" ]; then
        if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$rc" 2>/dev/null; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$rc"
        fi
    fi
done
echo "✓ CLI tool installed at ~/.local/bin/odoo-dev"

# 8. Dump MCP tool schemas
echo "📋 Step 7: Generating MCP Tool Schemas..."
python3 -c "
import asyncio, json, os, sys
sys.path.insert(0, os.path.expanduser('~/.gemini/config/plugins/odoo-dev'))
try:
    import mcp_server
    async def dump_schemas():
        tools = await mcp_server.server.list_tools()
        dirs = [
            os.path.expanduser('~/.gemini/antigravity/mcp/odoo-dev'),
            os.path.expanduser('~/.gemini/antigravity/mcp/odoo-dev_odoo-dev')
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)
            for tool in tools:
                t_dict = {
                    'name': tool.name,
                    'description': tool.description,
                    'parameters': tool.input_schema
                }
                with open(os.path.join(d, f'{tool.name}.json'), 'w') as f:
                    json.dump(t_dict, f, indent=2)
    asyncio.run(dump_schemas())
    print('✓ Live schemas dynamically generated.')
except Exception as e:
    print(f'Notice: dynamic schema generation skipped ({e}), deploying pre-packaged schemas...')
"

# Copy pre-packaged schemas as fallback/assurance
if [ -d "$SCRIPT_DIR/mcp-schemas" ]; then
    cp -r "$SCRIPT_DIR/mcp-schemas/"*.json "$HOME/.gemini/antigravity/mcp/odoo-dev/" 2>/dev/null || true
    cp -r "$SCRIPT_DIR/mcp-schemas/"*.json "$HOME/.gemini/antigravity/mcp/odoo-dev_odoo-dev/" 2>/dev/null || true
fi
echo "✓ MCP tool schemas ready."

# 9. Install Global Directives & Rules
echo "📜 Step 8: Installing Global AI Directives & Rules..."
cp "$SCRIPT_DIR/AGENTS.md" "$HOME/.gemini/config/AGENTS.md"
cp "$SCRIPT_DIR/GEMINI.md" "$HOME/.gemini/GEMINI.md"
mkdir -p "$HOME/.gemini/config/plugins/odoo-dev/rules"
cp "$SCRIPT_DIR/AGENTS.md" "$HOME/.gemini/config/plugins/odoo-dev/rules/AGENTS.md"

echo "✓ Global rules and directives installed."

echo ""
echo "=========================================================="
echo "🎉 SUCCESS: Private-Ai Suite is completely installed!"
echo "=========================================================="
echo "To verify:"
echo "  odoo-dev --help"
echo ""
echo "Restart your Antigravity / AI assistant session to activate all skills globally."
