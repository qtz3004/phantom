import logging
import os
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

import uvicorn
from ag_ui.core import RunAgentInput
from ag_ui.encoder import EventEncoder
from copilotkit import LangGraphAGUIAgent
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

# Gemini 응답의 ToolMessage.name이 None으로 들어올 때 ag_ui_langgraph의
# ToolCallStartEvent pydantic 검증이 실패하는 문제를 우회한다.
from langchain_core.messages import ToolMessage as _ToolMessage

_orig_tool_message_init = _ToolMessage.__init__


def _patched_tool_message_init(self, *args, **kwargs):
    _orig_tool_message_init(self, *args, **kwargs)
    if getattr(self, "name", None) is None:
        self.name = "tool"


_ToolMessage.__init__ = _patched_tool_message_init

from agent import agent

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "backend.log"

_log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
_file_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
)
_file_handler.setFormatter(logging.Formatter(_log_format))
_stream_handler = logging.StreamHandler()
_stream_handler.setFormatter(logging.Formatter(_log_format))

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    handlers=[_file_handler, _stream_handler],
    force=True,
)

for _uvicorn_logger in ("uvicorn", "uvicorn.error", "uvicorn.access"):
    _ul = logging.getLogger(_uvicorn_logger)
    _ul.handlers = [_file_handler, _stream_handler]
    _ul.propagate = False

logger = logging.getLogger("golden-cabbage")

app = FastAPI(title="황금배추 에이전트")

cors_origin = os.environ.get("CORS_ORIGIN", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[cors_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agui_agent = LangGraphAGUIAgent(
    name="golden-cabbage",
    description="황금배추 개인 비서 에이전트",
    graph=agent,
)


@app.post("/")
async def agent_endpoint(input_data: RunAgentInput, request: Request):
    # 사용자 질문 로깅
    for msg in reversed(input_data.messages):
        if msg.role == "user":
            content = getattr(msg, "content", None)
            if content:
                logger.info(f"[사용자 질문] {content}")
            break

    accept_header = request.headers.get("accept")
    encoder = EventEncoder(accept=accept_header)
    start = time.time()

    async def event_generator():
        text_parts = []
        async for event in agui_agent.run(input_data):
            # TextMessageContentEvent에서 최종 답변 수집
            event_type = getattr(event, "type", None)
            if event_type == "TEXT_MESSAGE_CONTENT":
                delta = getattr(event, "delta", "")
                if delta:
                    text_parts.append(delta)
            yield encoder.encode(event)

        # 스트림 종료 시 최종 답변 로깅
        elapsed = time.time() - start
        if text_parts:
            logger.info(f"[최종 답변] {''.join(text_parts)} ({elapsed:.2f}s)")
        else:
            logger.info(f"[최종 답변] (빈 응답) ({elapsed:.2f}s)")

    return StreamingResponse(
        event_generator(),
        media_type=encoder.get_content_type(),
    )


@app.get("/health")
def health():
    return {"status": "ok", "agent": {"name": agui_agent.name}}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)
