# Deep Agents 개요

> 계획 수립, 하위 에이전트 활용, 파일 시스템 활용이 가능한 에이전트 구축

LLM으로 구동되는 에이전트와 애플리케이션을 구축하는 가장 쉬운 방법으로, "작업 계획, 컨텍스트 관리용 파일 시스템, 하위 에이전트 생성, 장기 메모리"의 기능이 내장되어 있습니다.

`deepagents`는 "에이전트 하네스"로 생각할 수 있습니다. 다른 에이전트 프레임워크와 동일한 핵심 도구 호출 루프이지만 내장된 도구와 기능이 있습니다.

`deepagents` 라이브러리에는 다음이 포함됩니다:

* **Deep Agents SDK**: 모든 작업을 처리할 수 있는 에이전트 구축 패키지
* **Deep Agents CLI**: SDK 기반의 터미널 코딩 에이전트

## Deep Agents 생성

```python
# pip install -qU deepagents
from deepagents import create_deep_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_deep_agent(
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
```

## Deep Agents 사용 시기

**Deep Agents SDK** 사용:

* 계획 수립 및 분해가 필요한 복잡한 다단계 작업 처리
* 파일 시스템 도구를 통한 대량 컨텍스트 관리
* 메모리 내 상태, 로컬 디스크, 지속성 저장소, 샌드박스 또는 사용자 정의 백엔드로 파일시스템 백엔드 전환
* 컨텍스트 격리를 위해 특화된 하위 에이전트에 작업 위임
* 대화 및 스레드 전반에서 메모리 유지

더 간단한 에이전트의 경우 LangChain의 `create_agent`나 사용자 정의 LangGraph 워크플로우 구축을 고려하세요.

## 핵심 기능

**계획 및 작업 분해**
기본 `write_todos` 도구를 포함하여 에이전트가 복잡한 작업을 개별 단계로 분해하고, 진행 상황을 추적하며, 새로운 정보가 나타날 때 계획을 조정할 수 있게 합니다.

**컨텍스트 관리**
파일 시스템 도구(`ls`, `read_file`, `write_file`, `edit_file`)를 사용하면 에이전트가 대량 컨텍스트를 메모리 내 또는 파일시스템 저장소로 오프로드할 수 있습니다.

**플러그 가능한 파일시스템 백엔드**
메모리 내 상태, 로컬 디스크, 교차 스레드 지속성을 위한 LangGraph 저장소, 격리된 코드 실행(Modal, Daytona, Deno)용 샌드박스 중에서 선택하거나 복합 라우팅으로 여러 백엔드를 결합하세요.

**하위 에이전트 생성**
기본 `task` 도구를 사용하면 에이전트가 컨텍스트 격리를 위한 특화된 하위 에이전트를 생성할 수 있습니다.

**장기 메모리**
LangGraph의 메모리 저장소를 사용하여 스레드 전반에 걸친 지속적 메모리로 에이전트를 확장하세요.

## 문서 구조

| 페이지 | 경로 |
|--------|------|
| SDK 퀵스타트 | `/oss/python/deepagents/quickstart` |
| 커스터마이제이션 | `/oss/python/deepagents/customization` |
| 백엔드 | `/oss/python/deepagents/backends` |
| 샌드박스 | `/oss/python/deepagents/sandboxes` |
| 스킬 | `/oss/python/deepagents/skills` |
| 서브에이전트 | `/oss/python/deepagents/subagents` |
| 프론트엔드 | `/oss/python/deepagents/frontend/overview` |
| CLI 개요 | `/oss/python/deepagents/cli/overview` |
| API 레퍼런스 | `https://reference.langchain.com/python/deepagents/` |

> 원본: https://docs.langchain.com/oss/python/deepagents/overview
