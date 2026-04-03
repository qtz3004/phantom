import logging
import os
import time
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

if os.getenv("SSL_CERT_FILE"):
    os.environ.setdefault("REQUESTS_CA_BUNDLE", os.environ["SSL_CERT_FILE"])

from deepagents import create_deep_agent
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
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


class LoggingChatModel(ChatGoogleGenerativeAI):
    """모든 호출 경로(_generate/_agenerate/_stream/_astream)에서 로깅"""

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        _log_request(messages)
        start = time.time()
        result = super()._generate(messages, stop=stop, run_manager=run_manager, **kwargs)
        _log_response(result, time.time() - start)
        return result

    async def _agenerate(self, messages, stop=None, run_manager=None, **kwargs):
        _log_request(messages)
        start = time.time()
        result = await super()._agenerate(messages, stop=stop, run_manager=run_manager, **kwargs)
        _log_response(result, time.time() - start)
        return result

    def _stream(self, messages, stop=None, run_manager=None, **kwargs):
        _log_request(messages)
        start = time.time()
        chunks = []
        for chunk in super()._stream(messages, stop=stop, run_manager=run_manager, **kwargs):
            chunks.append(chunk)
            yield chunk
        elapsed = time.time() - start
        _log_stream_chunks(chunks, elapsed)

    async def _astream(self, messages, stop=None, run_manager=None, **kwargs):
        _log_request(messages)
        start = time.time()
        chunks = []
        async for chunk in super()._astream(messages, stop=stop, run_manager=run_manager, **kwargs):
            chunks.append(chunk)
            yield chunk
        elapsed = time.time() - start
        _log_stream_chunks(chunks, elapsed)


def get_current_time() -> str:
    """현재 날짜와 시간을 반환합니다."""
    return datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분 %S초")


SYSTEM_PROMPT = """당신은 황금배추라는 이름의 개인 비서 에이전트입니다.
사용자가 무엇을 물어보든 반드시 다음 두 가지를 포함하여 응답하세요:

1. "안녕하세요!" 인사
2. get_current_time 도구를 호출하여 현재 시간을 알려주기

예시 응답: "안녕하세요! 현재 시간은 2026년 04월 03일 14시 30분 00초입니다."

어떤 질문이든 이 형식으로만 응답하세요."""

llm = LoggingChatModel(model="gemini-3.1-flash-lite-preview")

agent = create_deep_agent(
    name="golden-cabbage",
    model=llm,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_current_time],
    checkpointer=MemorySaver(),
)
