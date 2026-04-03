# Frontend-Backend 연결 - CopilotKit + LangGraph

## 개요

CopilotKit은 Next.js frontend와 Python LangGraph backend를 **AG-UI protocol** (Server-Sent Events 기반)로 연결한다. 이 문서는 두 가지 연결 패턴을 설명한다.

## 아키텍처

```
┌─────────────────────┐     AG-UI (SSE)     ┌─────────────────────────┐
│  Next.js Frontend   │ ◄─────────────────► │  Python Backend         │
│                     │                      │                         │
│  <CopilotKit        │     HTTP POST       │  FastAPI                │
│    runtimeUrl=      │ ──────────────────► │    + LangGraphAGUIAgent │
│    "/api/copilotkit"│                      │    + LangGraph Graph    │
│  />                 │                      │                         │
│                     │                      │  Port: 8123             │
│  CopilotRuntime     │                      └─────────────────────────┘
│  (API Route)        │
│  Port: 3000         │
└─────────────────────┘
```

**연결 흐름:**
1. Frontend `<CopilotKit>` provider가 `/api/copilotkit`로 요청
2. Next.js API route의 `CopilotRuntime`이 요청을 Python backend로 프록시
3. Python backend에서 LangGraph agent 실행, SSE로 streaming 응답

## 방법 1: LangGraph 서버 방식 (langgraph-python)

LangGraph CLI/서버를 사용하여 agent를 호스팅하고, frontend에서 `LangGraphAgent`로 연결.

### Python Backend

**langgraph.json** (설정 파일):
```json
{
  "python_version": "3.12",
  "package_manager": "uv",
  "dependencies": ["."],
  "graphs": {
    "sample_agent": "./main.py:graph"
  },
  "env": "../../.env"
}
```

**main.py** (agent 정의):
```python
from copilotkit import CopilotKitMiddleware
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

agent = create_agent(
    model="openai:gpt-4.1",
    tools=[...],
    middleware=[CopilotKitMiddleware()],
    state_schema=AgentState,
)

graph = agent
```

LangGraph 서버 실행:
```bash
langgraph dev  # 기본 포트 8123
```

### Next.js Frontend API Route

```typescript
// src/app/api/copilotkit/route.ts
import {
  CopilotRuntime,
  ExperimentalEmptyAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { LangGraphAgent } from "@copilotkit/runtime/langgraph";
import { NextRequest } from "next/server";

const defaultAgent = new LangGraphAgent({
  deploymentUrl: process.env.LANGGRAPH_DEPLOYMENT_URL || "http://localhost:8123",
  graphId: "sample_agent",
  langsmithApiKey: process.env.LANGSMITH_API_KEY || "",
});

export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    endpoint: "/api/copilotkit",
    serviceAdapter: new ExperimentalEmptyAdapter(),
    runtime: new CopilotRuntime({
      agents: { default: defaultAgent },
    }),
  });

  return handleRequest(req);
};
```

**핵심 포인트:**
- `LangGraphAgent`: LangGraph 서버(langgraph dev)에 연결
- `deploymentUrl`: LangGraph 서버 주소
- `graphId`: `langgraph.json`의 graphs 키와 일치해야 함

## 방법 2: FastAPI 직접 호스팅 방식 (langgraph-fastapi) - 권장

FastAPI로 agent를 직접 호스팅하고, AG-UI protocol로 연결. LangGraph CLI 없이 독립 실행 가능.

### Python Backend

**agent 정의** (`src/agent.py`):
```python
from typing import List
from copilotkit import CopilotKitState
from langchain.tools import tool
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.types import Command
from typing_extensions import Literal


class AgentState(CopilotKitState):
    proverbs: List[str]


@tool
def get_weather(location: str):
    """주어진 위치의 날씨를 가져온다."""
    return f"{location}의 날씨: 21도"


tools = [get_weather]


async def chat_node(
    state: AgentState, config: RunnableConfig
) -> Command[Literal["tool_node", "__end__"]]:
    model = ChatOpenAI(model="gpt-4o")

    # Frontend action도 tool로 사용
    fe_tools = state.get("copilotkit", {}).get("actions", [])
    model_with_tools = model.bind_tools([*fe_tools, *tools])

    system_message = SystemMessage(content="당신은 도움이 되는 어시스턴트입니다.")

    response = await model_with_tools.ainvoke(
        [system_message, *state["messages"]], config
    )

    if response.tool_calls:
        return Command(goto="tool_node", update={"messages": response})
    return Command(goto="__end__", update={"messages": response})


workflow = StateGraph(AgentState)
workflow.add_node("chat_node", chat_node)
workflow.add_node("tool_node", ToolNode(tools=tools))
workflow.add_edge("tool_node", "chat_node")
workflow.set_entry_point("chat_node")

checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)
```

**FastAPI 서버** (`main.py`):
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

### Next.js Frontend API Route

```typescript
// src/app/api/copilotkit/route.ts
import {
  CopilotRuntime,
  ExperimentalEmptyAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { LangGraphHttpAgent } from "@copilotkit/runtime/langgraph";
import { NextRequest } from "next/server";

const serviceAdapter = new ExperimentalEmptyAdapter();

const runtime = new CopilotRuntime({
  agents: {
    sample_agent: new LangGraphHttpAgent({
      url: process.env.AGENT_URL || "http://localhost:8123",
    }),
  },
});

export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};
```

**핵심 차이점:**
- `LangGraphHttpAgent`: FastAPI 직접 호스팅된 agent에 연결 (AG-UI protocol)
- `LangGraphAgent`: LangGraph 서버(langgraph dev)에 연결
- agent 이름(`sample_agent`)이 Python과 TypeScript 양쪽에서 일치해야 함

### Frontend Layout

```tsx
// src/app/layout.tsx
import { CopilotKit } from "@copilotkit/react-core";

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <CopilotKit runtimeUrl="/api/copilotkit">
          {children}
        </CopilotKit>
      </body>
    </html>
  );
}
```

### Frontend Page

```tsx
"use client";
import { CopilotChat } from "@copilotkit/react-core/v2";

export default function HomePage() {
  return <CopilotChat />;
}
```

## 필수 패키지

### Python (Backend)

```toml
# pyproject.toml
[project]
requires-python = ">=3.12"
dependencies = [
    "copilotkit>=0.1.78",
    "fastapi>=0.115.5",
    "uvicorn>=0.29.0",
    "langgraph>=1.0.5",
    "langchain>=1.2.0",
    "langchain-openai>=1.1.0",
    "python-dotenv>=1.0.0",
]
```

### Next.js (Frontend)

```bash
npm install @copilotkit/react-core @copilotkit/runtime
```

## 환경 변수

```env
# Python Backend
OPENAI_API_KEY=sk-...
PORT=8123

# Next.js Frontend
AGENT_URL=http://localhost:8123          # FastAPI 방식
LANGGRAPH_DEPLOYMENT_URL=http://localhost:8123  # LangGraph 서버 방식
LANGSMITH_API_KEY=ls-...                 # optional
```

## 두 방식 비교

| 항목 | LangGraph 서버 방식 | FastAPI 직접 호스팅 방식 |
|------|---------------------|-------------------------|
| Python 엔트리 | `langgraph dev` | `uvicorn main:app` |
| Frontend agent 클래스 | `LangGraphAgent` | `LangGraphHttpAgent` |
| Python agent 클래스 | `CopilotKitMiddleware` | `LangGraphAGUIAgent` |
| 설정 파일 | `langgraph.json` 필요 | 불필요 |
| 프로토콜 | LangGraph 자체 | AG-UI (SSE) |
| 배포 유연성 | LangGraph Cloud 가능 | 아무 서버나 가능 |

## 연결 패턴 요약

1. **Python**: `CopilotKitState`를 상속한 state로 LangGraph graph 작성
2. **Python**: `LangGraphAGUIAgent`로 agent 래핑, FastAPI에 endpoint 등록
3. **Next.js**: API route에서 `CopilotRuntime` + `LangGraphHttpAgent`로 Python backend 연결
4. **Next.js**: `<CopilotKit runtimeUrl="/api/copilotkit">` provider로 앱 감싸기
5. **Next.js**: `<CopilotChat />` 등 UI 컴포넌트로 대화 인터페이스 구성

---

원본:
- https://docs.copilotkit.ai/coagents/quickstart/langgraph
- https://docs.copilotkit.ai/coagents/shared/guides/connect-to-langgraph
- https://github.com/CopilotKit/CopilotKit/tree/main/examples/integrations/langgraph-python
- https://github.com/CopilotKit/CopilotKit/tree/main/examples/integrations/langgraph-fastapi
