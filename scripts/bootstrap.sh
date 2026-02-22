#!/bin/bash
# E-Kashic Marketplace Bootstrap
# Run once to enable self-sync via MCP

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SERVER_PATH="$REPO_ROOT/marketplace/mcp/ekashic-manager/server.py"

echo "🌌 E-Kashic Bootstrap: Initializing..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv (Python package manager)..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

UV_PATH="$(which uv || echo "$HOME/.local/bin/uv")"

# Register ekashic-manager with uv
echo "🔗 Registering ekashic-manager MCP server..."
claude mcp add ekashic-manager -- "$UV_PATH" run --with mcp --with fastmcp python3 "$SERVER_PATH"

echo ""
echo "✅ Bootstrap complete."
echo ""
echo "Now use sync_ekashic_marketplace() in Claude Code to install all skills."
