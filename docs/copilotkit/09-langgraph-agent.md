# LangGraphAgent - LangGraph Agent 통합

## 개요

`LangGraphAgent`는 LangGraph로 작성된 workflow graph를 CopilotKit과 연결하는 클래스이다. Agent의 실행, 상태 관리, 메시지 변환, interrupt 처리를 담당한다.

## Agent 기본 클래스

모든 CopilotKit agent는 `Agent` base class를 상속한다.

```python
from copilotkit import Agent

class Agent:
    def __init__(self, name: str, description: Optional[str] = None):
        # name: 영문, 숫자, 언더스코어, 하이픈만 허용
        ...

    async def execute(self, state, config, messages, thread_id, actions, ...):
        """agent 실행 (abstract)"""
        ...

    async def get_state(self, thread_id) -> dict:
        """agent 상태 조회"""
        ...

    def dict_repr(self) -> AgentDict:
        """{"name": ..., "description": ...} 반환"""
        ...
```

## LangGraphAgent

### 생성자

```python
from copilotkit import LangGraphAgent

agent = LangGraphAgent(
    name="my_agent",           # agent 이름 (필수, 영문/숫자/_/- 만)
    description="설명",         # agent 설명 (optional)
    graph=compiled_graph,       # LangGraph compiled graph 객체
)
```

### 주요 기능

| 기능 | 설명 |
|------|------|
| Graph 실행 | LangGraph graph를 비동기 streaming으로 실행 |
| 메시지 변환 | CopilotKit <-> LangChain 메시지 포맷 자동 변환 |
| 상태 동기화 | Frontend와 agent 간 state 공유 |
| Interrupt 처리 | Human-in-the-loop workflow 지원 |
| Checkpoint | Thread 기반 상태 저장/복원 (time travel) |
| Intermediate state | 실행 중 중간 상태를 frontend로 streaming |

### CopilotKitConfig

Agent 동작을 커스터마이징하는 설정 TypedDict.

```python
from copilotkit.langgraph_agent import CopilotKitConfig

# state merge, message conversion 등의 hook 제공
```

## CopilotKitState

LangGraph의 `MessagesState`를 확장하여 CopilotKit 전용 필드를 추가한 state 클래스.

```python
from copilotkit import CopilotKitState
from typing import List

class AgentState(CopilotKitState):
    """
    CopilotKitState를 상속하면 copilotkit 관련 필드가 자동 포함된다.
    - messages: 대화 메시지 (MessagesState에서 상속)
    - copilotkit: CopilotKitProperties (actions, context 등)
    """
    # 커스텀 state 필드 추가
    proverbs: List[str]
```

**CopilotKitProperties 포함 항목:**

| 필드 | 설명 |
|------|------|
| `actions` | Frontend에서 정의된 action (tool) 목록 |
| `context` | Context item 목록 (description + value) |

## LangGraph Graph 작성 예시

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
    return f"{location}의 날씨: 21도, 맑음"


tools = [get_weather]


async def chat_node(
    state: AgentState, config: RunnableConfig
) -> Command[Literal["tool_node", "__end__"]]:
    model = ChatOpenAI(model="gpt-4o")

    # Frontend에서 정의된 action도 tool로 바인딩
    fe_tools = state.get("copilotkit", {}).get("actions", [])
    model_with_tools = model.bind_tools([*fe_tools, *tools])

    system_message = SystemMessage(
        content=f"당신은 도움이 되는 어시스턴트입니다. 현재 속담: {state.get('proverbs', [])}"
    )

    response = await model_with_tools.ainvoke(
        [system_message, *state["messages"]],
        config,
    )

    # Tool call이 있으면 tool_node로, 없으면 종료
    if response.tool_calls:
        return Command(goto="tool_node", update={"messages": response})
    return Command(goto="__end__", update={"messages": response})


# Graph 정의
workflow = StateGraph(AgentState)
workflow.add_node("chat_node", chat_node)
workflow.add_node("tool_node", ToolNode(tools=tools))
workflow.add_edge("tool_node", "chat_node")
workflow.set_entry_point("chat_node")

checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)
```

## LangGraph 유틸리티 함수

`copilotkit.langgraph` 모듈에서 제공하는 유틸리티:

```python
from copilotkit.langgraph import (
    copilotkit_customize_config,   # LangGraph config에 CopilotKit 메타데이터 추가
    copilotkit_emit_state,         # 중간 상태를 frontend로 streaming
    copilotkit_emit_message,       # 실행 중 사용자에게 메시지 전송
    copilotkit_emit_tool_call,     # 수동 tool call 트리거
    copilotkit_exit,               # agent 종료 신호
    copilotkit_interrupt,          # 실행 일시정지, 사용자 입력 대기
)
```

### 사용 예시

```python
from copilotkit.langgraph import copilotkit_emit_state, copilotkit_interrupt

async def my_node(state, config):
    # 중간 상태를 frontend에 전달
    await copilotkit_emit_state(config, {"progress": 50})

    # 사용자 입력을 기다림 (human-in-the-loop)
    user_input = await copilotkit_interrupt(config, "계속 진행하시겠습니까?")

    return {"messages": [...]}
```

## LangGraphAGUIAgent (최신)

AG-UI protocol 기반의 최신 agent 클래스. `LangGraphAgent` 대신 사용 권장.

```python
from copilotkit import LangGraphAGUIAgent

agent = LangGraphAGUIAgent(
    name="sample_agent",
    description="샘플 에이전트",
    graph=graph,
)
```

## CopilotKitMiddleware

LangChain의 `create_agent()`와 함께 사용하는 미들웨어.

```python
from copilotkit import CopilotKitMiddleware
from langchain.agents import create_agent

agent = create_agent(
    model="openai:gpt-4.1",
    tools=[...],
    middleware=[CopilotKitMiddleware()],
    state_schema=AgentState,
)

graph = agent  # create_agent의 반환값을 그대로 graph로 사용
```

---

원본: https://docs.copilotkit.ai/reference/sdk/python/LangGraphAgent
소스코드: https://github.com/CopilotKit/CopilotKit/blob/main/sdk-python/copilotkit/langgraph_agent.py
