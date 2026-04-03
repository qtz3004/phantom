# CopilotKit Python SDK - Backend 설정

## 개요

CopilotKit Python SDK는 Python으로 작성된 action과 agent를 CopilotKit 프론트엔드 애플리케이션에 연결하는 backend 구성요소이다.

## 설치

```bash
pip install copilotkit
```

CrewAI 통합이 필요한 경우:
```bash
pip install "copilotkit[crewai]"
```

**Python 요구사항**: >=3.10, <3.13

## 핵심 클래스

### CopilotKitRemoteEndpoint

Python backend에서 action과 agent를 등록하고 CopilotKit Runtime에 노출하는 메인 클래스.

> `CopilotKitSDK`는 v0.1.31부터 deprecated. `CopilotKitRemoteEndpoint`를 사용할 것.

```python
from copilotkit import CopilotKitRemoteEndpoint, LangGraphAgent

sdk = CopilotKitRemoteEndpoint(
    agents=[
        LangGraphAgent(
            name="my_agent",
            description="에이전트 설명",
            graph=graph,  # LangGraph compiled graph
        )
    ],
    actions=[],  # optional: Action 목록
)
```

**생성자 파라미터:**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| `agents` | `list[Agent]` 또는 `Callable` | 등록할 agent 목록. context를 받아 동적으로 반환하는 callable도 가능 |
| `actions` | `list[Action]` 또는 `Callable` | 등록할 action 목록. callable 지원 |

**주요 메서드:**

| 메서드 | 설명 |
|--------|------|
| `info()` | SDK 메타데이터, 등록된 action/agent 목록 반환 |
| `execute_action(name, args)` | 지정된 action 실행 |
| `execute_agent(name, thread_id, state, messages)` | agent 실행 (streaming 응답) |
| `get_agent_state(name, thread_id)` | agent의 현재 상태 조회 |

### CopilotKitContext

요청 context를 담는 TypedDict. 동적 agent/action 등록 시 사용한다.

```python
# 동적 agent 등록 예시 - context 기반 필터링
def get_agents(context: CopilotKitContext):
    # context.properties, context.frontend_url, context.headers 사용 가능
    return [my_agent]

sdk = CopilotKitRemoteEndpoint(agents=get_agents)
```

## FastAPI 통합

`add_fastapi_endpoint()`로 FastAPI 앱에 CopilotKit endpoint를 등록한다.

```python
from fastapi import FastAPI
from copilotkit.integrations.fastapi import add_fastapi_endpoint

app = FastAPI()

add_fastapi_endpoint(app, sdk, "/copilotkit")
```

**등록되는 endpoint:**

| 경로 | 메서드 | 설명 |
|------|--------|------|
| `/copilotkit/` | GET | SDK 메타데이터 (info) |
| `/copilotkit/action/{name}` | POST | Action 실행 |
| `/copilotkit/agent/{name}` | POST | Agent 실행 (SSE streaming) |
| `/copilotkit/agent/{name}/state` | POST | Agent 상태 조회 |

## AG-UI 방식 (최신 권장)

최신 CopilotKit은 AG-UI protocol 기반의 `LangGraphAGUIAgent`와 `add_langgraph_fastapi_endpoint`를 권장한다.

```python
import os
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from copilotkit import LangGraphAGUIAgent
from ag_ui_langgraph import add_langgraph_fastapi_endpoint
from src.agent import graph

load_dotenv()
app = FastAPI()

add_langgraph_fastapi_endpoint(
    app=app,
    agent=LangGraphAGUIAgent(
        name="sample_agent",
        description="샘플 에이전트",
        graph=graph,
    ),
    path="/",
)

def main():
    port = int(os.getenv("PORT", "8123"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

if __name__ == "__main__":
    main()
```

## SDK Export 목록

```python
from copilotkit import (
    CopilotKitRemoteEndpoint,  # Remote endpoint (메인 클래스)
    CopilotKitSDK,             # deprecated, RemoteEndpoint 사용
    CopilotKitContext,         # 요청 context
    Agent,                     # Agent base class
    LangGraphAgent,            # LangGraph 통합 agent
    LangGraphAGUIAgent,        # LangGraph AG-UI agent (최신)
    Action,                    # Action 정의
    Parameter,                 # 파라미터 정의
    CopilotKitState,           # LangGraph state에 CopilotKit 필드 추가
    CopilotKitMiddleware,      # 미들웨어
)
```

## 주요 의존성

| 패키지 | 용도 |
|--------|------|
| `copilotkit` | CopilotKit Python SDK |
| `fastapi` | 웹 프레임워크 |
| `uvicorn` | ASGI 서버 |
| `langgraph` | LangGraph workflow |
| `langchain` / `langchain-openai` | LLM 통합 |
| `ag-ui-langgraph` | AG-UI protocol LangGraph 통합 |

---

원본: https://docs.copilotkit.ai/reference/sdk/python/CopilotKitRemoteEndpoint
소스코드: https://github.com/CopilotKit/CopilotKit/tree/main/sdk-python/copilotkit
