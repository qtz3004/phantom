# CoAgents - LangGraph 연동 Quickstart

LangChain/LangGraph 에이전트를 CopilotKit과 연동하여 에이전트 네이티브 애플리케이션을 구축하는 가이드.

## 사전 요구사항

- OpenAI API key
- Node.js 20+
- (선택) LangSmith API key — 기존 LangChain 에이전트 사용 시 필요

## 방법 1: CLI로 빠르게 시작

```bash
# Python 에이전트
npx copilotkit@latest create -f langgraph-py

# JavaScript 에이전트
npx copilotkit@latest create -f langgraph-js
```

```bash
npm install
```

`.env` 파일 생성:

```plaintext title=".env"
OPENAI_API_KEY=your_openai_api_key
```

```bash
npm run dev
```

## 방법 2: 기존 에이전트에 통합

### Step 1: 에이전트 프로젝트 초기화

```bash
uv init my-agent
cd my-agent
```

### Step 2: 패키지 설치

```bash
uv add langgraph copilotkit langchain-openai langchain-core
```

### Step 3: 에이전트 작성 및 AG-UI 노출

AG-UI는 프론트엔드-에이전트 통신을 위한 오픈 프로토콜이다.

#### LangSmith 배포 방식

에이전트 코드:

```python title="main.py"
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph

async def mock_llm(state: MessagesState):
  model = ChatOpenAI(model="gpt-4.1-mini")
  system_message = SystemMessage(content="You are a helpful assistant.")
  response = await model.ainvoke(
    [
      system_message,
      *state["messages"],
    ]
  )
  return {"messages": response}

graph = StateGraph(MessagesState)
graph.add_node(mock_llm)
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)
graph = graph.compile()
```

LangGraph 설정 파일:

```json title="langgraph.json"
{
  "python_version": "3.12",
  "dockerfile_lines": [],
  "dependencies": ["."],
  "package_manager": "uv",
  "graphs": {
    "sample_agent": "./main.py:graph"
  },
  "env": ".env"
}
```

#### FastAPI 배포 방식

추가 패키지:

```bash
uv add ag-ui-langgraph fastapi uvicorn copilotkit
```

```python title="main.py"
import os
from ag_ui_langgraph import add_langgraph_fastapi_endpoint
from copilotkit import LangGraphAGUIAgent
from fastapi import FastAPI
from langgraph.graph import END, START, MessagesState, StateGraph
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

async def mock_llm(state: MessagesState):
  model = ChatOpenAI(model="gpt-4.1-mini")
  system_message = SystemMessage(content="You are a helpful assistant.")
  response = await model.ainvoke(
    [
      system_message,
      *state["messages"],
    ]
  )
  return {"messages": response}

graph = StateGraph(MessagesState)
graph.add_node(mock_llm)
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)
graph = graph.compile()

app = FastAPI()

add_langgraph_fastapi_endpoint(
  app=app,
  agent=LangGraphAGUIAgent(
    name="sample_agent",
    description="An example agent to use as a starting point for your own agent.",
    graph=graph,
  ),
  path="/",
)

def main():
  """Run the uvicorn server."""
  uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port="8123",
    reload=True,
  )

if __name__ == "__main__":
  main()
```

### Step 4: 프론트엔드 생성

```bash
npx create-next-app@latest frontend
cd frontend
npm install @copilotkit/react-ui @copilotkit/react-core @copilotkit/runtime
```

### Step 5: Copilot Runtime API Route

#### LangSmith 방식

```tsx title="app/api/copilotkit/route.ts"
import {
  CopilotRuntime,
  ExperimentalEmptyAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { LangGraphAgent } from "@copilotkit/runtime/langgraph";
import { NextRequest } from "next/server";

const serviceAdapter = new ExperimentalEmptyAdapter();

const runtime = new CopilotRuntime({
  agents: {
    sample_agent: new LangGraphAgent({
      deploymentUrl: process.env.LANGGRAPH_DEPLOYMENT_URL || "http://localhost:8123",
      graphId: "sample_agent",
      langsmithApiKey: process.env.LANGSMITH_API_KEY || "",
    }),
  }
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

#### FastAPI 방식

```tsx title="app/api/copilotkit/route.ts"
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
      url: process.env.LANGGRAPH_DEPLOYMENT_URL || "http://localhost:8123",
    }),
  }
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

### Step 6: CopilotKit Provider 설정

```tsx title="app/layout.tsx"
import { CopilotKit } from "@copilotkit/react-core";
import "@copilotkit/react-ui/v2/styles.css";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <CopilotKit runtimeUrl="/api/copilotkit" agent="sample_agent">
          {children}
        </CopilotKit>
      </body>
    </html>
  );
}
```

### Step 7: Chat UI 추가

```tsx title="app/page.tsx"
import { CopilotSidebar } from "@copilotkit/react-core/v2";

export default function Page() {
  return (
    <main>
      <h1>Your App</h1>
      <CopilotSidebar />
    </main>
  );
}
```

### Step 8: 서버 시작

에이전트 서버 (LangSmith):

```bash
npx @langchain/langgraph-cli dev --port 8123 --no-browser
```

에이전트 서버 (FastAPI):

```bash
uv run main.py
```

프론트엔드:

```bash
cd frontend
npm run dev
```

## 핵심 패키지 정리

| 패키지 | 역할 |
|--------|------|
| `langgraph` | LangGraph 에이전트 프레임워크 |
| `copilotkit` | Python SDK (LangGraphAGUIAgent 등) |
| `langchain-openai` | OpenAI LLM 연동 |
| `ag-ui-langgraph` | LangGraph를 AG-UI 엔드포인트로 노출 |
| `@copilotkit/runtime` | 백엔드 런타임 |
| `@copilotkit/react-core` | React Provider 및 hooks |
| `@copilotkit/react-ui` | 사전 빌드된 UI 컴포넌트 |

## 핵심 클래스 비교

| 클래스 | 배포 방식 | 설명 |
|--------|-----------|------|
| `LangGraphAgent` | LangSmith | LangSmith 배포된 에이전트 연결 |
| `LangGraphHttpAgent` | FastAPI | 자체 호스팅 HTTP 에이전트 연결 |
| `LangGraphAGUIAgent` | Python 측 | AG-UI 엔드포인트로 에이전트 래핑 |

## 트러블슈팅

- 연결 문제: `0.0.0.0` 또는 `127.0.0.1`을 `localhost` 대신 사용
- `langgraph.json` 파일이 에이전트 폴더에 있는지 확인
- `.env` 파일 경로가 `langgraph.json`에서 올바르게 참조되는지 확인
- Runtime endpoint 경로와 `runtimeUrl`이 일치하는지 확인

## 다음 단계

- **Human in the Loop**: 사용자와 에이전트 협업
- **Shared State**: 에이전트 상태와 UI 상태 동기화
- **Generative UI**: 에이전트 진행 상황을 UI에 렌더링
- **Frontend Tools**: 에이전트가 프론트엔드 도구를 직접 호출

---

원본: https://docs.copilotkit.ai/coagents/quickstart/langgraph
