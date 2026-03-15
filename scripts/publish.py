#!/usr/bin/env python3
"""
E-Kashic Publish Script
~/.ekashic/ 로그를 ekashic 저장소로 병합 동기화
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

# 경로 설정
HOME = Path.home()
LOCAL_EKASHIC = HOME / ".ekashic"
REPO_ROOT = Path(__file__).parent.parent
REPO_DATA = REPO_ROOT / "data"


def parse_insight_table(content: str) -> tuple[str, list[str]]:
    """인사이트 마크다운에서 헤더와 데이터 행 분리"""
    lines = content.strip().split("\n")
    header_lines = []
    data_rows = []

    for i, line in enumerate(lines):
        # 테이블 데이터 행 (| 로 시작하고 Timestamp가 아니고 :---가 아닌 행)
        if line.startswith("|"):
            if "Timestamp" in line or ":---" in line:
                header_lines.append(line)
            else:
                data_rows.append(line)
        else:
            header_lines.append(line)

    return "\n".join(header_lines), data_rows


def extract_timestamp(row: str) -> str:
    """테이블 행에서 Timestamp 추출"""
    match = re.search(r"\|\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\s*\|", row)
    return match.group(1) if match else ""


def merge_insight_files(local_path: Path, remote_path: Path) -> str:
    """두 인사이트 파일을 병합"""
    local_content = local_path.read_text() if local_path.exists() else ""
    remote_content = remote_path.read_text() if remote_path.exists() else ""

    if not local_content and not remote_content:
        return ""

    if not remote_content:
        return local_content

    if not local_content:
        return remote_content

    # 헤더와 데이터 분리
    local_header, local_rows = parse_insight_table(local_content)
    remote_header, remote_rows = parse_insight_table(remote_content)

    # 행 병합 (중복 제거)
    all_rows = {}
    for row in remote_rows + local_rows:
        ts = extract_timestamp(row)
        if ts:
            all_rows[ts] = row  # 같은 timestamp면 로컬이 우선

    # Timestamp 기준 정렬
    sorted_rows = sorted(all_rows.values(), key=extract_timestamp)

    # 결과 조합
    result = local_header if local_header else remote_header
    if sorted_rows:
        result += "\n" + "\n".join(sorted_rows) + "\n"

    return result


def sync_insights():
    """인사이트 디렉토리 병합 동기화"""
    local_dir = LOCAL_EKASHIC / "insights"
    remote_dir = REPO_DATA / "insights"

    if not local_dir.exists():
        print("  [skip] 로컬 insights 디렉토리 없음")
        return

    remote_dir.mkdir(parents=True, exist_ok=True)

    # 모든 .md 파일 수집
    all_files = set()
    if local_dir.exists():
        all_files.update(f.name for f in local_dir.glob("*.md"))
    if remote_dir.exists():
        all_files.update(f.name for f in remote_dir.glob("*.md"))

    for filename in sorted(all_files):
        local_path = local_dir / filename
        remote_path = remote_dir / filename

        merged = merge_insight_files(local_path, remote_path)
        if merged:
            remote_path.write_text(merged)
            status = "merged" if remote_path.exists() and local_path.exists() else "added"
            print(f"  [{status}] insights/{filename}")


def sync_archive():
    """아카이브 디렉토리 동기화 (파일 단위)"""
    local_dir = LOCAL_EKASHIC / "archive"
    remote_dir = REPO_DATA / "archive"

    if not local_dir.exists():
        print("  [skip] 로컬 archive 디렉토리 없음")
        return

    remote_dir.mkdir(parents=True, exist_ok=True)

    for local_file in local_dir.glob("*.md"):
        remote_file = remote_dir / local_file.name

        if remote_file.exists():
            # 내용 비교
            local_content = local_file.read_text()
            remote_content = remote_file.read_text()

            if local_content == remote_content:
                print(f"  [unchanged] archive/{local_file.name}")
            else:
                # 다른 경우: 로컬 우선 (더 최신이라고 가정)
                shutil.copy2(local_file, remote_file)
                print(f"  [updated] archive/{local_file.name}")
        else:
            shutil.copy2(local_file, remote_file)
            print(f"  [added] archive/{local_file.name}")


def main():
    print("=" * 50)
    print("E-Kashic Publish")
    print("=" * 50)
    print(f"\n소스: {LOCAL_EKASHIC}")
    print(f"대상: {REPO_DATA}\n")

    if not LOCAL_EKASHIC.exists():
        print("Error: ~/.ekashic 디렉토리가 없습니다.")
        return 1

    # 데이터 디렉토리 생성
    REPO_DATA.mkdir(parents=True, exist_ok=True)

    print("[Insights 동기화]")
    sync_insights()

    print("\n[Archive 동기화]")
    sync_archive()

    print("\n" + "=" * 50)
    print("동기화 완료!")
    print("=" * 50)
    print("\n다음 단계:")
    print(f"  cd {REPO_ROOT}")
    print("  git status")
    print("  git diff data/")
    print('  git add data/ && git commit -m "docs: update ekashic logs"')
    print("  git push")

    return 0


if __name__ == "__main__":
    exit(main())
