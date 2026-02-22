import os
import re
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Writing-Agent")

# 경로 설정
REPO_ROOT = Path(__file__).parent.parent.parent.parent
POSTS_DIR = REPO_ROOT / "resource" / "posts"
AGENTS_DIR = REPO_ROOT / "agents" / "writing-agent"


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """YAML 프론트매터와 본문 분리"""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            import yaml
            try:
                metadata = yaml.safe_load(parts[1])
                body = parts[2].strip()
                return metadata or {}, body
            except:
                pass
    return {}, content


def search_in_file(file_path: Path, keywords: list[str]) -> int:
    """파일에서 키워드 매칭 점수 계산"""
    try:
        content = file_path.read_text(encoding='utf-8')
        metadata, body = parse_frontmatter(content)

        score = 0
        search_text = f"{metadata.get('title', '')} {metadata.get('tags', [])} {body}".lower()

        for keyword in keywords:
            if keyword.lower() in search_text:
                # 제목에 있으면 가중치 높음
                if keyword.lower() in str(metadata.get('title', '')).lower():
                    score += 3
                # 태그에 있으면 가중치 높음
                if keyword.lower() in str(metadata.get('tags', [])).lower():
                    score += 2
                # 본문에 있으면 기본 점수
                if keyword.lower() in body.lower():
                    score += 1
        return score
    except:
        return 0


@mcp.tool()
def search_writings(keywords: list[str], source: str = "all", limit: int = 3) -> str:
    """
    키워드로 과거 글 검색
    Args:
        keywords: 검색 키워드 리스트
        source: "linkedin", "blog", "all"
        limit: 반환 개수 (기본 3)
    Returns:
        관련 글 내용 (제목, 태그, 본문 요약)
    """
    results = []

    # 검색 대상 디렉토리 결정
    dirs_to_search = []
    if source in ["linkedin", "all"]:
        dirs_to_search.append(POSTS_DIR / "linked-in")
    if source in ["blog", "all"]:
        dirs_to_search.append(POSTS_DIR / "blog")

    # 모든 MD 파일 검색
    for search_dir in dirs_to_search:
        if search_dir.exists():
            for md_file in search_dir.glob("*.md"):
                score = search_in_file(md_file, keywords)
                if score > 0:
                    content = md_file.read_text(encoding='utf-8')
                    metadata, body = parse_frontmatter(content)
                    results.append({
                        'file': md_file.name,
                        'score': score,
                        'title': metadata.get('title', md_file.stem),
                        'tags': metadata.get('tags', []),
                        'source': metadata.get('source', search_dir.name),
                        'body': body[:500] + "..." if len(body) > 500 else body
                    })

    # 점수순 정렬 및 상위 N개 반환
    results.sort(key=lambda x: x['score'], reverse=True)
    top_results = results[:limit]

    if not top_results:
        return f"키워드 {keywords}와 관련된 글을 찾지 못했습니다."

    output = []
    for r in top_results:
        output.append(f"## {r['title']}\n- 태그: {r['tags']}\n- 출처: {r['source']}\n\n{r['body']}\n")

    return "\n---\n".join(output)


@mcp.tool()
def get_writing_persona() -> str:
    """Ethan의 글쓰기 페르소나 반환"""
    persona_path = AGENTS_DIR / "PERSONA.md"
    if persona_path.exists():
        return persona_path.read_text(encoding='utf-8')
    return "페르소나 파일을 찾을 수 없습니다."


@mcp.tool()
def get_platform_rules(platform: str) -> str:
    """
    플랫폼별 글쓰기 규칙 반환
    Args:
        platform: "linkedin" 또는 "blog"
    """
    rules_path = AGENTS_DIR / "platforms" / f"{platform}.md"
    if rules_path.exists():
        return rules_path.read_text(encoding='utf-8')
    return f"{platform} 플랫폼 규칙 파일을 찾을 수 없습니다."


@mcp.tool()
def list_writing_sources() -> str:
    """사용 가능한 글 소스 목록 및 통계 반환"""
    stats = {}

    for source_dir in POSTS_DIR.iterdir():
        if source_dir.is_dir():
            md_files = list(source_dir.glob("*.md"))
            stats[source_dir.name] = len(md_files)

    if not stats:
        return "등록된 글이 없습니다."

    output = "## 글 저장소 현황\n"
    for source, count in stats.items():
        output += f"- {source}: {count}개\n"

    return output


if __name__ == "__main__":
    mcp.run()
