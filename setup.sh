#!/bin/bash

# 1. 경로 설정
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_DIR="$HOME/.config/ai"

echo "🚀 AI Context 설정 시작..."

# 2. 설정 디렉토리 생성 (없을 경우)
mkdir -p "$CONFIG_DIR"

# 3. 공통 설정 (SOUL.md) 연결
# -f 옵션은 기존에 링크가 있으면 덮어씁니다.
ln -sf "$REPO_DIR/core/SOUL.md" "$CONFIG_DIR/SOUL.md"
echo "✅ SOUL.md 연결 완료"

# 4. 노트북 환경 선택
echo "-----------------------------------"
echo "현재 노트북의 환경을 선택해주세요:"
echo "1) 업무용 (Work)"
echo "2) 개인용 (Personal)"
read -p "번호 입력 (1 or 2): " ENV_CHOICE

if [ "$ENV_CHOICE" == "1" ]; then
    ln -sf "$REPO_DIR/work/ENV.md" "$CONFIG_DIR/ENV.md"
    echo "✅ 업무용(Work) ENV.md 연결 완료"
elif [ "$ENV_CHOICE" == "2" ]; then
    ln -sf "$REPO_DIR/personal/ENV.md" "$CONFIG_DIR/ENV.md"
    echo "✅ 개인용(Personal) ENV.md 연결 완료"
else
    echo "❌ 잘못된 선택입니다. ENV.md 연결을 건너뜁니다."
fi

echo "-----------------------------------"
echo "✨ 모든 설정이 완료되었습니다!"
echo "AI 에이전트가 '$CONFIG_DIR' 경로를 참조하도록 설정하세요."
