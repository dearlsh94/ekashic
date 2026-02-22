import os
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# Initialize E-Kashic Specialized Server
mcp = FastMCP("E-Kashic-Core")

@mcp.tool()
def ekashic_archive(title: str, content: str) -> str:
    """
    E-Kashic Archiver: Saves Ethan's strategic decisions and plan summaries.
    Args:
        title: Hyphenated title (e.g., 'setup-ekashic-system').
        content: Detailed summary including Objective, Decisions, and Impact.
    """
    date_prefix = datetime.now().strftime("%Y-%m-%d")
    safe_title = "".join([c if c.isalnum() or c == "-" else "-" for c in title.lower()])
    
    plan_dir = os.path.expanduser("~/.ai/ekashic")
    os.makedirs(plan_dir, exist_ok=True)

    file_path = os.path.join(plan_dir, f"{date_prefix}-{safe_title}.md")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return f"🌌 E-Kashic: Archive successfully stored for Ethan at {file_path}"

if __name__ == "__main__":
    mcp.run()
