"""고유가 피해 지원금 서브에이전트 도구 — TOC 검색 및 본문 Grab"""

import re
from pathlib import Path

DOCS_DIR = Path(__file__).parent / "docs"


def _extract_headers(file_path: Path) -> list[str]:
    """파일에서 헤더 라인만 추출한다."""
    lines = file_path.read_text(encoding="utf-8").splitlines()
    filename = ""
    for line in lines:
        if line.startswith("# "):
            match = re.search(r"파일명:\s*(\S+)", line)
            if match:
                filename = match.group(1)
            break

    result = []
    for i, line in enumerate(lines, start=1):
        if line.startswith("#"):
            # 파일명이 없는 헤더에 추가
            if filename and "파일명:" not in line and "| 라인:" in line:
                line = line.replace("| 라인:", f"| 파일명: {filename} | 라인:", 1)
            result.append(f"L{i}: {line}")
    return result


def search_docs() -> str:
    """문서 폴더에서 목차(TOC)를 반환합니다.

    docs/tocs.md 파일이 있으면 그대로 반환하고,
    없으면 모든 문서에서 헤더를 추출합니다.
    """
    if not DOCS_DIR.exists():
        return "문서 폴더가 비어있습니다."

    tocs_file = DOCS_DIR / "tocs.md"
    if tocs_file.exists():
        content = tocs_file.read_text(encoding="utf-8").strip()
        if content:
            return content

    md_files = sorted(f for f in DOCS_DIR.rglob("*.md") if f.name != "tocs.md")
    if not md_files:
        return "문서 폴더에 파일이 없습니다."

    toc_parts = []
    for md_file in md_files:
        headers = _extract_headers(md_file)
        if headers:
            toc_parts.extend(headers)

    if not toc_parts:
        return "문서에서 헤더를 찾을 수 없습니다."

    return "\n".join(toc_parts)


def _find_file(filename: str) -> Path | None:
    """docs/ 폴더를 재귀 탐색하여 파일을 찾는다."""
    if not DOCS_DIR.exists():
        return None
    for path in DOCS_DIR.rglob(filename):
        return path
    for path in DOCS_DIR.rglob(f"*{filename}*"):
        return path
    return None


def _grab_lines(file_path: Path, start: int, end: int) -> str:
    """파일에서 지정 라인 범위를 추출한다. (1-based)"""
    lines = file_path.read_text(encoding="utf-8").splitlines()
    return "\n".join(lines[start - 1 : end])


def grab_section(select_expression: str) -> str:
    """선택된 섹션의 본문과 참조를 추출합니다.

    search_docs로 TOC를 확인한 후, 관련 섹션을 다음 형식으로 전달하세요:
    "파일명 | 라인: start-end | 참조: ref_start-ref_end"

    여러 섹션은 줄바꿈으로 구분합니다.

    Args:
        select_expression: "422767515.md | 라인: 6-17 | 참조: 3-4" 형식의 문자열
    """
    pattern = r"(\S+\.md)\s*\|\s*라인:\s*(\d+)-(\d+)\s*\|\s*참조:\s*(\d+)-(\d+)"
    matches = list(re.finditer(pattern, select_expression))

    if not matches:
        return "올바른 형식이 아닙니다. '파일명 | 라인: start-end | 참조: ref_start-ref_end' 형식으로 입력하세요."

    parts = []
    for match in matches:
        filename = match.group(1)
        line_start, line_end = int(match.group(2)), int(match.group(3))
        ref_start, ref_end = int(match.group(4)), int(match.group(5))

        file_path = _find_file(filename)
        if not file_path:
            parts.append(f"해당 문서({filename})를 찾을 수 없어 답변할 수 없습니다.")
            continue

        body = _grab_lines(file_path, line_start, line_end)
        ref = _grab_lines(file_path, ref_start, ref_end)
        parts.append(f"[본문] ({filename}, 라인 {line_start}-{line_end})\n{body}\n\n[참조] ({filename}, 라인 {ref_start}-{ref_end})\n{ref}")

    return "\n\n---\n\n".join(parts)
