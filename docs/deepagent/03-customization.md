# 커스터마이제이션

## 기본 함수 서명

```python
create_deep_agent(
    name: str | None = None,
    model: str | BaseChatModel | None = None,
    tools: Sequence[BaseTool | Callable | dict[str, Any]] | None = None,
    *,
    system_prompt: str | SystemMessage | None = None
) -> CompiledStateGraph
```

## 연결 복원력

LangChain 채팅 모델은 실패한 API 요청을 지수 백오프로 자동 재시도합니다. 기본값으로 네트워크 오류, 속도 제한(429), 서버 오류(5xx)에 대해 **최대 6회** 재시도합니다.

```python
from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent

agent = create_deep_agent(
    model=init_chat_model(
        model="claude-sonnet-4-6",
        max_retries=10,
        timeout=120,
    ),
)
```

## 모델

기본값은 `claude-sonnet-4-6`. 지원되는 모델 식별자 문자열 또는 LangChain 모델 객체를 전달할 수 있습니다.

### 지원 프로바이더

| 프로바이더 | 설치 | 모델 예시 |
|-----------|------|-----------|
| OpenAI | `pip install -U "langchain[openai]"` | `openai:gpt-5.2` |
| Anthropic | `pip install -U "langchain[anthropic]"` | `claude-sonnet-4-6` |
| Azure | `pip install -U "langchain[openai]"` | `azure_openai:gpt-5.2` |
| Google Gemini | `pip install -U "langchain[google-genai]"` | `google_genai:gemini-2.5-flash-lite` |
| AWS Bedrock | `pip install -U "langchain[aws]"` | `anthropic.claude-3-5-sonnet-20240620-v1:0` |
| HuggingFace | `pip install -U "langchain[huggingface]"` | `microsoft/Phi-3-mini-4k-instruct` |

## 도구 (Tools)

기본 제공되는 도구 외에 커스텀 도구를 제공할 수 있습니다:

```python
from deepagents import create_deep_agent

def internet_search(query: str, max_results: int = 5):
    """웹 검색 실행"""
    ...

agent = create_deep_agent(tools=[internet_search])
```

## 시스템 프롬프트

```python
agent = create_deep_agent(
    system_prompt="당신은 전문 연구원입니다.",
)
```

## 미들웨어 (Middleware)

기본 미들웨어:
- `TodoListMiddleware`: 작업 추적 및 관리
- `FilesystemMiddleware`: 파일 시스템 작업 처리
- `SubAgentMiddleware`: 서브에이전트 생성 및 조율
- `SummarizationMiddleware`: 메시지 히스토리 압축
- `AnthropicPromptCachingMiddleware`: Anthropic 모델 토큰 중복 처리
- `PatchToolCallsMiddleware`: 중단된 도구 호출 메시지 히스토리 자동 수정

추가 미들웨어 (조건부):
- `MemoryMiddleware`: `memory` 인수 제공 시
- `SkillsMiddleware`: `skills` 인수 제공 시
- `HumanInTheLoopMiddleware`: `interruptOn` 인수 제공 시

### 커스텀 미들웨어

```python
from langchain.tools import tool
from langchain.agents.middleware import wrap_tool_call
from deepagents import create_deep_agent

@wrap_tool_call
def log_tool_calls(request, handler):
    """모든 도구 호출 기록"""
    print(f"[Middleware] 도구 호출: {request.name}")
    result = handler(request)
    return result

agent = create_deep_agent(
    tools=[get_weather],
    middleware=[log_tool_calls],
)
```

> **주의**: 초기화 후 속성을 변경하지 마세요. 값 추적이 필요하면 그래프 상태를 사용하세요.

## 서브에이전트 (Subagents)

```python
research_subagent = {
    "name": "research-agent",
    "description": "더 심화된 질문 연구에 사용",
    "system_prompt": "당신은 훌륭한 연구원입니다",
    "tools": [internet_search],
    "model": "openai:gpt-5.2",  # 선택사항
}

agent = create_deep_agent(
    model="claude-sonnet-4-6",
    subagents=[research_subagent]
)
```

## 백엔드 (Backends)

| 백엔드 | 설명 |
|--------|------|
| `StateBackend` | 기본값. LangGraph 상태에 저장된 임시 파일시스템 |
| `FilesystemBackend` | 로컬 디스크 파일시스템 |
| `LocalShellBackend` | 파일시스템 + 셸 실행 (`execute` 도구) |
| `StoreBackend` | 스레드 간 지속되는 장기 저장소 |
| `CompositeBackend` | 경로별 다른 백엔드 라우팅 |

## 인간 개입 (Human-in-the-loop)

```python
from langgraph.checkpoint.memory import MemorySaver

agent = create_deep_agent(
    tools=[delete_file, read_file, send_email],
    interrupt_on={
        "delete_file": True,
        "read_file": False,
        "send_email": {"allowed_decisions": ["approve", "reject"]},
    },
    checkpointer=MemorySaver(),
)
```

## 스킬 (Skills)

스킬을 사용하여 Deep Agent에 새로운 기능과 전문 지식을 제공. 도구가 저수준 기능을 다루는 반면, 스킬은 작업 완료 방법에 대한 상세한 지침을 포함합니다.

```python
agent = create_deep_agent(
    skills=["/skills/"],
    checkpointer=checkpointer,
)
```

## 메모리 (Memory)

`AGENTS.md` 파일을 사용하여 추가 컨텍스트를 제공합니다:

```python
agent = create_deep_agent(
    memory=["/AGENTS.md"],
    checkpointer=checkpointer,
)
```

## 구조화된 출력 (Structured Output)

```python
from pydantic import BaseModel, Field

class WeatherReport(BaseModel):
    location: str = Field(description="위치")
    temperature: float = Field(description="섭씨 온도")
    condition: str = Field(description="날씨 상태")

agent = create_deep_agent(
    response_format=WeatherReport,
    tools=[internet_search]
)

result = agent.invoke({...})
print(result["structured_response"])
```

> 원본: https://docs.langchain.com/oss/python/deepagents/customization
