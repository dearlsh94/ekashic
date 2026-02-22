#!/bin/bash
# Path: scripts/ekashic.sh
# Description: E-Kashic Marketplace Manager (Install & Sync)

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REGISTRY="$REPO_ROOT/marketplace/registry.json"

echo "🌌 E-Kashic Marketplace: Synchronizing Skills..."

# 1. Dependency Check
if ! pip list | grep -q "fastmcp"; then
    echo "📦 Installing FastMCP..."
    pip install mcp fastmcp
fi

# 2. Parse Registry and Register to Claude Code
# We use python3 to parse JSON safely without requiring 'jq'
python3 <<EOF
import json
import subprocess
import os

with open('$REGISTRY', 'r') as f:
    data = json.load(f)
    for skill in data['skills']:
        skill_id = skill['id']
        # Convert relative path to absolute path
        abs_path = os.path.abspath(os.path.join('$REPO_ROOT', skill['path']))
        
        print(f"🔗 Registering: {skill['name']} ({skill_id})")
        
        # Execute Claude config command
        cmd = ["claude", "config", "add", "mcp-server", skill_id, "--", "python3", abs_path]
        subprocess.run(cmd)

print("\n✅ E-Kashic: All skills are synchronized with Claude Code.")
EOF
