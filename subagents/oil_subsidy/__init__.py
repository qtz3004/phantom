"""고유가 피해 지원금 안내 서브에이전트"""

import logging

from langchain.agents.middleware import wrap_model_call
from langchain_core.messages import AIMessage

from prompts import load_prompt
from .middleware import search_docs, grab_section

logger = logging.getLogger("oil-subsidy-middleware")


def _extract_text(content) -> str:
    """AIMessage.content에서 텍스트를 추출한다. str 또는 list[dict] 형태 모두 처리."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("text"):
                parts.append(item["text"])
            elif isinstance(item, str):
                parts.append(item)
        return "\n".join(parts)
    return str(content) if content else ""


@wrap_model_call
async def toc_middleware(request, handler):
    """Before: TOC 주입 → LLM: SELECT 선택 → After: 본문+참조 grab"""
    # Before Hook: TOC 주입
    toc = search_docs()
    if toc and "헤더를 찾을 수 없습니다" not in toc:
        request = request.override(
            messages=request.messages + [
                {"role": "user", "content": f"[참고 문서 목차]\n{toc}"},
            ]
        )
    logger.info("[Before Hook] TOC 주입 완료")

    # LLM 처리
    result = await handler(request)

    # After Hook: result에서 content 추출
    content = ""
    if isinstance(result, AIMessage):
        content = _extract_text(result.content)
    else:
        # ModelResponse.result → list[BaseMessage]
        msgs = getattr(result, "result", None)
        if isinstance(msgs, list):
            for msg in msgs:
                if hasattr(msg, "content") and msg.content:
                    content = _extract_text(msg.content)
                    break

    logger.info(f"[After Hook] content: {content[:200]}")

    if "SELECT:" in content:
        select_lines = [
            line.replace("SELECT:", "").strip()
            for line in content.splitlines()
            if line.strip().startswith("SELECT:")
        ]
        if select_lines:
            select_expression = "\n".join(select_lines)
            grabbed = grab_section(select_expression)
            logger.info(f"[After Hook] grab 완료: {grabbed[:200]}")
            grabbed_msg = AIMessage(content=grabbed)
            if isinstance(result, AIMessage):
                return grabbed_msg
            from langchain.agents.middleware.types import ModelResponse
            return ModelResponse(result=[grabbed_msg])

    return result


_prompt = load_prompt("oil_subsidy_guide")

oil_subsidy_subagent = {
    "name": _prompt["name"],
    "description": _prompt["description"],
    "system_prompt": _prompt["system_prompt"],
    "tools": [],
    "middleware": [toc_middleware],
}
