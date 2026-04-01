# Subagents

Deep Agents는 작업을 위임하기 위해 subagents를 생성합니다. 컨텍스트 격리와 특화된 지침 제공에 유용합니다.

## 사용 시기

- ✅ 메인 agent의 컨텍스트를 복잡하게 만드는 다단계 작업
- ✅ 커스텀 지침이나 도구가 필요한 특화 영역
- ✅ 다양한 모델 기능이 필요한 작업
- ❌ 단순하고 단일 단계의 작업
- ❌ 중간 컨텍스트 유지가 필요한 경우

## SubAgent 딕셔너리

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `name` | `str` | O | 고유 식별자 |
| `description` | `str` | O | 수행 작업 설명 |
| `system_prompt` | `str` | O | 지침 (메인에서 상속 안됨) |
| `tools` | `list[Callable]` | O | 사용 가능한 도구 |
| `model` | `str \| BaseChatModel` | X | 모델 오버라이드 |
| `middleware` | `list[Middleware]` | X | 커스텀 미들웨어 |
| `interrupt_on` | `dict[str, bool]` | X | HITL 설정 |
| `skills` | `list[str]` | X | 스킬 소스 경로 |

```python
research_subagent = {
    "name": "research-agent",
    "description": "Used to research more in depth questions",
    "system_prompt": "You are a great researcher",
    "tools": [internet_search],
    "model": "openai:gpt-5.2",
}

agent = create_deep_agent(
    model="claude-sonnet-4-6",
    subagents=[research_subagent]
)
```

## CompiledSubAgent

사전 구축된 LangGraph 그래프 사용:

```python
from deepagents import create_deep_agent, CompiledSubAgent

custom_subagent = CompiledSubAgent(
    name="data-analyzer",
    description="Specialized agent for complex data analysis tasks",
    runnable=custom_graph
)

agent = create_deep_agent(subagents=[custom_subagent])
```

## General-Purpose Subagent

항상 사용 가능. 메인 에이전트와 동일한 시스템 프롬프트, 도구, 모델, 스킬을 가짐.

오버라이드 방법:

```python
agent = create_deep_agent(
    model="claude-sonnet-4-6",
    subagents=[{
        "name": "general-purpose",
        "description": "General-purpose agent for research and multi-step tasks",
        "system_prompt": "You are a general-purpose assistant.",
        "tools": [internet_search],
        "model": "openai:gpt-4o",
    }],
)
```

## 컨텍스트 관리

부모 agent의 runtime context가 자동으로 모든 subagents로 전파됩니다.

```python
agent = create_deep_agent(
    subagents=[research_subagent],
    context_schema={"user_id": str, "session_id": str},
)

result = await agent.invoke(
    {"messages": [HumanMessage("Look up my recent activity")]},
    {"context": {"user_id": "user-123", "session_id": "abc"}},
)
```

### Subagent별 컨텍스트 (네임스페이스 키)

```python
result = await agent.invoke(
    {"messages": [...]},
    {"context": {
        "user_id": "user-123",              # 모든 agents 공유
        "researcher:max_depth": 3,           # researcher만
        "fact-checker:strict_mode": True,    # fact-checker만
    }},
)
```

## 모범 사례

1. **명확한 설명**: `"Analyzes financial data and generates investment insights"` (O) vs `"Does finance stuff"` (X)
2. **상세한 시스템 프롬프트**: 출력 형식, 단어 제한 등 명시
3. **도구 세트 최소화**: 관련 도구만 포함
4. **작업별 모델 선택**: 긴 문서용 큰 컨텍스트 모델, 수치 분석용 별도 모델 등
5. **간결한 결과 반환**: 원시 데이터, 중간 계산 제외

## 일반 패턴: 다중 특화 Subagents

```python
subagents = [
    {"name": "data-collector", "description": "Gathers raw data", "tools": [web_search, api_call]},
    {"name": "data-analyzer", "description": "Analyzes data for insights", "tools": [statistical_analysis]},
    {"name": "report-writer", "description": "Writes polished reports", "tools": [format_document]},
]

agent = create_deep_agent(
    system_prompt="You coordinate data analysis and reporting.",
    subagents=subagents
)
```

> 원본: https://docs.langchain.com/oss/python/deepagents/subagents
