import logging
import os
import time
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

# 회사 프록시 SSL 인증서 설정
if os.getenv("SSL_CERT_FILE"):
    os.environ.setdefault("REQUESTS_CA_BUNDLE", os.environ["SSL_CERT_FILE"])

from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.checkpoint.memory import MemorySaver

from prompts import load_prompt
from subagents import knowledge_search_subagent

_log_handlers = [logging.StreamHandler()]
_log_dir = os.getenv("LOG_DIR")
if _log_dir:
    os.makedirs(_log_dir, exist_ok=True)
    _log_handlers.append(logging.FileHandler(f"{_log_dir}/agent.log", encoding="utf-8"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=_log_handlers,
)
logger = logging.getLogger("golden-cabbage")


def _log_request(messages):
    """마지막 메시지 기준으로 로깅 (사용자 질문 or 도구 결과)"""
    for msg in reversed(messages):
        if isinstance(msg, ToolMessage):
            logger.info(f"[LLM 요청] 도구 결과({msg.name}) → {msg.content}")
            return
        if isinstance(msg, HumanMessage):
            logger.info(f"[LLM 요청] {msg.content}")
            return


def _log_stream_chunks(chunks, elapsed):
    """스트리밍 청크를 모아서 최종 응답 로깅"""
    from langchain_core.outputs import ChatGenerationChunk

    text_parts = []
    tool_names = []
    for chunk in chunks:
        if isinstance(chunk, ChatGenerationChunk):
            msg = chunk.message
        else:
            msg = chunk
        if hasattr(msg, "content") and msg.content:
            content = msg.content
            if isinstance(content, str):
                text_parts.append(content)
            elif isinstance(content, list):
                for part in content:
                    if isinstance(part, dict) and part.get("text"):
                        text_parts.append(part["text"])
            else:
                text_parts.append(str(content))
        if hasattr(msg, "tool_call_chunks"):
            for tc in msg.tool_call_chunks:
                if tc.get("name"):
                    tool_names.append(tc["name"])

    if text_parts:
        logger.info(f"[LLM 응답] {''.join(text_parts)} ({elapsed:.2f}s)")
    if tool_names:
        logger.info(f"[LLM 도구호출] {', '.join(dict.fromkeys(tool_names))} ({elapsed:.2f}s)")
    if not text_parts and not tool_names:
        logger.info(f"[LLM 응답] (스트리밍 빈 응답) ({elapsed:.2f}s)")


def _log_response(result, elapsed):
    """LLM 응답 로깅 (텍스트 + 도구 호출)"""
    logged = False
    for gen in result.generations:
        msg = getattr(gen, "message", None)
        if gen.text:
            logger.info(f"[LLM 응답] {gen.text} ({elapsed:.2f}s)")
            logged = True
        elif isinstance(msg, AIMessage):
            if msg.content:
                logger.info(f"[LLM 응답] {msg.content} ({elapsed:.2f}s)")
                logged = True
            if msg.tool_calls:
                names = ", ".join(tc["name"] for tc in msg.tool_calls)
                logger.info(f"[LLM 도구호출] {names} ({elapsed:.2f}s)")
                logged = True
    if not logged:
        logger.info(f"[LLM 응답] (빈 응답) ({elapsed:.2f}s)")


def get_current_time() -> str:
    """현재 날짜와 시간을 반환합니다."""
    return datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분 %S초")


MODEL = "google_genai:gemini-3.1-flash-lite-preview"

llm = init_chat_model(MODEL)
# 서브에이전트용 비스트리밍 모델 — SELECT 토큰이 UI로 새지 않도록 함
subagent_llm = init_chat_model(MODEL, disable_streaming=True)
knowledge_search_subagent["model"] = subagent_llm

orchestrator = load_prompt("orchestrator")

agent = create_deep_agent(
    name=orchestrator["name"],
    model=llm,
    system_prompt=orchestrator["system_prompt"],
    tools=[get_current_time],
    backend=None,
    checkpointer=MemorySaver(),
    subagents=[knowledge_search_subagent],
)
