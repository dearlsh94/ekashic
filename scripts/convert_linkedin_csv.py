#!/usr/bin/env python3
"""
LinkedIn CSV를 개별 MD 파일로 변환
"""

import csv
import re
import unicodedata
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).parent.parent
CSV_PATH = REPO_ROOT / "resource" / "posts" / "linkedIn" / "260315-LinkedIn-Shares.csv"
OUTPUT_DIR = REPO_ROOT / "resource" / "posts" / "linkedIn"


def slugify(text: str, max_length: int = 50) -> str:
    """텍스트를 파일명에 적합한 slug로 변환"""
    # 특수문자 제거, 공백을 하이픈으로
    text = re.sub(r'[^\w\s가-힣-]', '', text)
    text = re.sub(r'\s+', '-', text.strip())
    text = text.lower()

    # 길이 제한
    if len(text) > max_length:
        text = text[:max_length].rsplit('-', 1)[0]

    return text or "untitled"


def extract_title(commentary: str) -> str:
    """글 본문에서 제목 추출 (첫 줄 또는 첫 문장)"""
    # 빈 줄로 분리된 첫 번째 단락
    lines = commentary.strip().split('\n')
    first_line = lines[0].strip().strip('"')

    # 너무 길면 자르기
    if len(first_line) > 60:
        # 첫 문장 추출
        match = re.match(r'^(.{10,60})[.!?]', first_line)
        if match:
            return match.group(1)
        return first_line[:60] + "..."

    return first_line


def extract_tags(commentary: str) -> list[str]:
    """글 내용에서 태그 추출 (해시태그 또는 주요 키워드)"""
    tags = []

    # 해시태그 추출
    hashtags = re.findall(r'#(\w+)', commentary)
    tags.extend(hashtags[:5])

    # 키워드 기반 태그 (자주 등장하는 주제들)
    keyword_map = {
        'react': ['React', 'react', 'useEffect', 'useState', 'React Query'],
        'typescript': ['TypeScript', 'typescript', '타입'],
        'frontend': ['프론트엔드', 'frontend', 'CSS', 'UI'],
        'backend': ['백엔드', 'backend', 'API', '서버'],
        'leadership': ['리더십', 'leadership', '리더', '팀장'],
        'book': ['책', '읽고', '독서', '독후감'],
        'ai': ['AI', 'ChatGPT', 'Claude', '인공지능'],
        'career': ['커리어', '이직', '성장', '개발자'],
        'architecture': ['아키텍처', '설계', '도메인', 'DDD'],
        'communication': ['소통', '커뮤니케이션', '협업'],
    }

    commentary_lower = commentary.lower()
    for tag, keywords in keyword_map.items():
        if any(kw.lower() in commentary_lower for kw in keywords):
            if tag not in tags:
                tags.append(tag)

    return tags[:5]  # 최대 5개


def clean_commentary(text: str) -> str:
    """CSV에서 읽은 본문 정리"""
    # 연속된 따옴표 처리
    text = text.replace('""', '"')
    # 앞뒤 따옴표 제거
    text = text.strip().strip('"')
    # 각 줄 앞뒤의 따옴표 제거
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip().strip('"')
        cleaned_lines.append(line)
    text = '\n'.join(cleaned_lines)
    # 줄바꿈 정규화
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def convert_csv_to_md():
    """CSV 파일을 개별 MD 파일로 변환"""
    if not CSV_PATH.exists():
        print(f"Error: CSV 파일을 찾을 수 없습니다: {CSV_PATH}")
        return 1

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    converted = 0
    skipped = 0

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        # 모든 행을 메모리에 로드하고 날짜 파싱
        rows = []
        for row in reader:
            if not row.get('ShareCommentary', '').strip():
                continue

            try:
                # 날짜 파싱
                date_str = row['Date']
                dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                rows.append((dt, row))
            except (ValueError, KeyError):
                continue

        # 같은 날짜의 글들 그룹화 (인덱스 부여용)
        date_counts = {}

        for dt, row in rows:
            date_key = dt.strftime('%Y-%m-%d')
            date_counts[date_key] = date_counts.get(date_key, 0) + 1

        # 같은 날짜 내에서 인덱스 추적
        date_indices = {}

        for dt, row in rows:
            commentary = clean_commentary(row['ShareCommentary'])
            if not commentary:
                skipped += 1
                continue

            title = extract_title(commentary)
            tags = extract_tags(commentary)

            date_key = dt.strftime('%Y-%m-%d')

            # 같은 날짜에 여러 글이 있으면 인덱스 추가
            if date_counts[date_key] > 1:
                date_indices[date_key] = date_indices.get(date_key, 0) + 1
                idx = date_indices[date_key]
                slug = slugify(title)
                filename = f"{date_key}-{idx:02d}-{slug}.md"
            else:
                slug = slugify(title)
                filename = f"{date_key}-{slug}.md"

            output_path = OUTPUT_DIR / filename

            # MD 파일 생성
            md_content = f"""---
title: "{title}"
date: {dt.strftime('%Y-%m-%d %H:%M')}
source: linkedin
link: {row.get('ShareLink', '')}
tags: {tags}
---

{commentary}
"""

            output_path.write_text(md_content, encoding='utf-8')
            converted += 1

            if converted <= 5:
                print(f"  [created] {filename}")

        if converted > 5:
            print(f"  ... and {converted - 5} more files")

    print(f"\n변환 완료: {converted}개 생성, {skipped}개 스킵")
    return 0


if __name__ == "__main__":
    print("=" * 50)
    print("LinkedIn CSV → MD 변환")
    print("=" * 50)
    print(f"\n입력: {CSV_PATH}")
    print(f"출력: {OUTPUT_DIR}\n")

    exit(convert_csv_to_md())
