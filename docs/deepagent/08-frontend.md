# Frontend

실시간 서브에이전트 스트림, 작업 진행률, 샌드박스를 표시하는 UI를 구축합니다.

## 아키텍처

Deep Agents는 조정자-워커(coordinator-worker) 아키텍처를 사용합니다. 메인 에이전트가 작업을 계획하고 각각 격리된 상태에서 실행되는 특화된 서브에이전트에 위임합니다.

```
FRONTEND (useStream) <-> BACKEND (createDeepAgent)
                           |
                    Subagent A, B
```

### Python 백엔드

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
    subagents=[{"name": "researcher", "description": "Research assistant"}],
)
```

### TypeScript 프론트엔드

```typescript
import { useStream } from "@langchain/react";

function App() {
  const stream = useStream<typeof agent>({
    apiUrl: "http://localhost:2024",
    assistantId: "agent",
  });

  const todos = stream.values?.todos;
  const subagents = stream.subagents;
}
```

## UI 패턴

| 패턴 | 설명 | 경로 |
|------|------|------|
| Subagent Streaming | 스트리밍 콘텐츠, 진행 추적, 축소 가능한 카드 | `/frontend/subagent-streaming` |
| Todo List | 에이전트 상태와 동기화된 실시간 작업 목록 | `/frontend/todo-list` |
| Sandbox | 파일 브라우저, 코드 뷰어, 차이점 패널이 있는 IDE 같은 UI | `/frontend/sandbox` |

LangChain 프론트엔드 패턴(마크다운 메시지, 도구 호출, HITL)은 모두 Deep Agents와도 작동합니다. 동일한 LangGraph 런타임 위에 구축되어 `useStream`은 동일한 핵심 API를 제공합니다.

> 원본: https://docs.langchain.com/oss/python/deepagents/frontend/overview
