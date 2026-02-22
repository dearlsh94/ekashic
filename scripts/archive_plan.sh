#!/bin/bash
# Path: scripts/archive_plan.sh

DATE=$(date +%Y-%m-%d)
TITLE=${1:-"unnamed-plan"}
SAFE_TITLE=$(echo "$TITLE" | sed 's/[^a-zA-Z0-9-]/-/g' | tr '[:upper:]' '[:lower:]')
PLAN_DIR="./.ai/plans"
FILE_PATH="$PLAN_DIR/$DATE-$SAFE_TITLE.md"

mkdir -p "$PLAN_DIR"

# Read from stdin and save to file
cat > "$FILE_PATH"

echo "Successfully archived to $FILE_PATH"
