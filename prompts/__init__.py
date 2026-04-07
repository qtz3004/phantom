from pathlib import Path

PROMPTS_DIR = Path(__file__).parent


def load_prompt(name: str) -> dict:
    """prompts/ 디렉토리에서 마크다운 프롬프트 파일을 읽어 반환합니다.

    파일 형식:
        ---
        name: agent-name
        description: 에이전트 설명
        ---
        시스템 프롬프트 본문...

    Returns:
        {"name": str, "description": str, "system_prompt": str}
    """
    path = PROMPTS_DIR / f"{name}.md"
    text = path.read_text(encoding="utf-8")

    if text.startswith("---"):
        _, frontmatter, body = text.split("---", 2)
        meta = {}
        for line in frontmatter.strip().splitlines():
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
        meta["system_prompt"] = body.strip()
        return meta

    return {"system_prompt": text}
