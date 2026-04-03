import logging
import time

import uvicorn
from ag_ui.core import RunAgentInput
from ag_ui.encoder import EventEncoder
from copilotkit import LangGraphAGUIAgent
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

from agent import agent

logger = logging.getLogger("golden-cabbage")

app = FastAPI(title="황금배추 에이전트")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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
    uvicorn.run(app, host="0.0.0.0", port=8123)
