#!/bin/bash

# 1. 경로 설정 (Path Configuration)
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_DIR="$HOME/.config/ekashic"

echo "🚀 AI Context Setup Starting..."
echo "-----------------------------------"

# 2. 설정 디렉토리 생성 (Ensure Config Directory Exists)
mkdir -p "$CONFIG_DIR"

# 3. 공통 파일 연결 (Link Common Files)
# Layer 1: Global Philosophy
ln -sf "$REPO_DIR/core/SOUL.md" "$CONFIG_DIR/SOUL.md"
echo "✅ Linked: SOUL.md (Global Philosophy)"

# Layer 4: Assistant Rules
ln -sf "$REPO_DIR/agents/my-assistant/RULES.md" "$CONFIG_DIR/AGENT_RULES.md"
echo "✅ Linked: AGENT_RULES.md (Assistant Persona)"

# 4. 환경 선택 및 개발 규칙 연결 (Environment-Specific Setup)
echo "-----------------------------------"
echo "Select your environment for DEV_RULES:"
echo "1) Work (업무용)"
echo "2) Personal (개인용)"
read -p "Enter number (1 or 2): " ENV_CHOICE

if [ "$ENV_CHOICE" == "1" ]; then
    ln -sf "$REPO_DIR/domains/work/DEV_RULES.md" "$CONFIG_DIR/DEV_RULES.md"
    echo "✅ Linked: domains/work/DEV_RULES.md -> DEV_RULES.md"
elif [ "$ENV_CHOICE" == "2" ]; then
    ln -sf "$REPO_DIR/domains/personal/DEV_RULES.md" "$CONFIG_DIR/DEV_RULES.md"
    echo "✅ Linked: domains/personal/DEV_RULES.md -> DEV_RULES.md"
else
    echo "❌ Invalid choice. Skipping DEV_RULES setup."
fi

echo "-----------------------------------"
echo "✨ Setup Complete!"
echo "Your AI contexts are now synced at: $CONFIG_DIR"
