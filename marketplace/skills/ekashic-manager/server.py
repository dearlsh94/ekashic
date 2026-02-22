import subprocess
import json
import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("E-Kashic-Manager")

# 스크립트 위치 기준으로 리포지토리 루트 계산
# server.py → ekashic-manager/ → skills/ → marketplace/ → repo_root
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

@mcp.tool()
def sync_ekashic_marketplace() -> str:
    """
    Scans the E-Kashic registry and automatically registers all skills to Claude Code.
    Use this when you want to update or install the entire marketplace.
    """
    registry_path = os.path.join(REPO_ROOT, "marketplace/registry.json")

    # Find uv path
    uv_path = os.path.expanduser("~/.local/bin/uv")
    if not os.path.exists(uv_path):
        import shutil
        uv_path = shutil.which("uv")
    if not uv_path:
        return "❌ Error: uv not found. Please install uv first: curl -LsSf https://astral.sh/uv/install.sh | sh"

    with open(registry_path, 'r') as f:
        data = json.load(f)
        results = []
        for skill in data['skills']:
            abs_path = os.path.join(REPO_ROOT, skill['path'])
            # Use uv run --with mcp --with fastmcp to handle dependencies automatically
            cmd = ["claude", "mcp", "add", skill['id'], "--", uv_path, "run", "--with", "mcp", "--with", "fastmcp", "python3", abs_path]
            subprocess.run(cmd, check=True)
            results.append(skill['id'])

    return f"✅ E-Kashic Sync Complete. Skills registered: {', '.join(results)}"

if __name__ == "__main__":
    mcp.run()
