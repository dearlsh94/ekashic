import subprocess
import json
import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("E-Kashic-Manager")

@mcp.tool()
def sync_ekashic_marketplace() -> str:
    """
    Scans the E-Kashic registry and automatically registers all skills to Claude Code.
    Use this when you want to update or install the entire marketplace.
    """
    repo_root = os.path.expanduser("~/projects/dotfiles-ai")
    registry_path = os.path.join(repo_root, "marketplace/registry.json")
    
    with open(registry_path, 'r') as f:
        data = json.load(f)
        results = []
        for skill in data['skills']:
            abs_path = os.path.join(repo_root, skill['path'])
            # Command to register the skill to Claude Code
            cmd = f"claude config add mcp-server {skill['id']} -- python3 {abs_path}"
            subprocess.run(cmd, shell=True, check=True)
            results.append(skill['id'])
            
    return f"✅ E-Kashic Sync Complete. Skills registered: {', '.join(results)}"
