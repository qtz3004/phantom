"""Markdown 파일에서 헤더만 추출하여 목차 파일을 생성하는 도구"""

import re
from pathlib import Path

# wiki-crawler 출력 디렉토리 기본 경로
CRAWLER_OUTPUT_DIR = Path(__file__).parent.parent / ".claude" / "skills" / "wiki-crawler" / "output"
HEADER_OUTPUT_DIR = Path(__file__).parent.parent / ".claude" / "skills" / "header-extractor" / "output"


def _extract_filename(lines: list[str]) -> str:
    """h1 헤더에서 파일명을 추출한다."""
    for line in lines:
        if line.startswith("# "):
            match = re.search(r"파일명:\s*(\S+)", line)
            if match:
                return match.group(1)
    return ""


def _ensure_filename_in_header(line: str, filename: str) -> str:
    """헤더에 파일명이 없으면 추가한다."""
    if not filename or "파일명:" in line:
        return line

    # ## 제목 | 라인: x-y | 참조: a-b → ## 제목 | 파일명: xxx.md | 라인: x-y | 참조: a-b
    if "| 라인:" in line:
        return line.replace("| 라인:", f"| 파일명: {filename} | 라인:", 1)

    return line


def extract_headers(file_path: str) -> str:
    """Markdown 파일에서 #, ##, ### 헤더만 추출하여 목차 파일로 저장합니다.

    전체 파일을 읽지 않고 헤더(목차)만 먼저 확인하여 토큰을 절감합니다.
    반환된 헤더의 '라인:' 범위로 필요한 섹션만 선택적으로 읽을 수 있습니다.

    Args:
        file_path: 읽을 Markdown 파일 경로.
            파일명만 전달하면 wiki-crawler 출력 디렉토리에서 검색합니다.
    """
    path = Path(file_path)

    if not path.is_absolute() and not path.exists():
        candidate = CRAWLER_OUTPUT_DIR / file_path
        if candidate.exists():
            path = candidate
        else:
            matches = list(CRAWLER_OUTPUT_DIR.glob(f"*{file_path}*"))
            if matches:
                path = matches[0]
            else:
                return f"파일을 찾을 수 없습니다: {file_path}"

    if not path.exists():
        return f"파일을 찾을 수 없습니다: {path}"

    lines = path.read_text(encoding="utf-8").splitlines()
    filename = _extract_filename(lines)

    result = []
    for i, line in enumerate(lines, start=1):
        if line.startswith("#"):
            header = _ensure_filename_in_header(line, filename)
            result.append(f"L{i}: {header}")

    if not result:
        return f"헤더를 찾을 수 없습니다: {path.name}"

    output = "\n".join(result)

    # 결과 파일 저장
    HEADER_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_filename = filename if filename else path.name
    out_path = HEADER_OUTPUT_DIR / out_filename
    out_path.write_text(output, encoding="utf-8")

    return output
