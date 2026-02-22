import subprocess
import json
import os
import shutil
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("E-Kashic-Manager")

# 스크립트 위치 기준으로 리포지토리 루트 계산
# server.py → ekashic-manager/ → mcp/ → marketplace/ → repo_root
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

@mcp.tool()
def sync_ekashic_marketplace() -> str:
    """
    Scans the E-Kashic registry and automatically registers all skills to Claude Code.
    - Skills (Markdown): Copies to ~/.claude/skills/
    - Commands (Markdown): Copies to ~/.claude/commands/
    - MCP servers: Registers via claude mcp add
    """
    registry_path = os.path.join(REPO_ROOT, "marketplace/registry.json")
    results = {"skills": [], "commands": [], "mcp": []}

    with open(registry_path, 'r') as f:
        data = json.load(f)

    # 1. Skills → ~/.claude/skills/ (Claude 제안용)
    skills_dir = os.path.expanduser("~/.claude/skills")
    os.makedirs(skills_dir, exist_ok=True)

    for skill in data.get('skills', []):
        src_path = os.path.join(REPO_ROOT, skill['path'])
        shutil.copy2(src_path, os.path.join(skills_dir, f"{skill['id']}.md"))
        results["skills"].append(skill['id'])

    # 2. Commands → ~/.claude/commands/ (사용자 /명령어 호출용)
    commands_dir = os.path.expanduser("~/.claude/commands")
    os.makedirs(commands_dir, exist_ok=True)

    for cmd in data.get('commands', []):
        src_path = os.path.join(REPO_ROOT, cmd['path'])
        shutil.copy2(src_path, os.path.join(commands_dir, f"{cmd['id']}.md"))
        results["commands"].append(cmd['id'])

    # 3. MCP servers
    uv_path = os.path.expanduser("~/.local/bin/uv")
    if not os.path.exists(uv_path):
        uv_path = shutil.which("uv")

    if data.get('mcp') and not uv_path:
        return "❌ Error: uv not found. Install: curl -LsSf https://astral.sh/uv/install.sh | sh"

    for mcp_server in data.get('mcp', []):
        abs_path = os.path.join(REPO_ROOT, mcp_server['path'])
        # Remove existing MCP server first (ignore errors if not exists)
        subprocess.run(["claude", "mcp", "remove", mcp_server['id']], capture_output=True)
        # Add MCP server
        cmd = ["claude", "mcp", "add", mcp_server['id'], "--",
               uv_path, "run", "--with", "mcp", "--with", "fastmcp", "python3", abs_path]
        subprocess.run(cmd, check=True)
        results["mcp"].append(mcp_server['id'])

    summary = []
    if results["skills"]:
        summary.append(f"Skills: {', '.join(results['skills'])}")
    if results["commands"]:
        summary.append(f"Commands: {', '.join(results['commands'])}")
    if results["mcp"]:
        summary.append(f"MCP: {', '.join(results['mcp'])}")

    return f"✅ E-Kashic Sync Complete.\n" + "\n".join(summary)

if __name__ == "__main__":
    mcp.run()
