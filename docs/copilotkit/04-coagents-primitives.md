# CoAgents Shared State Primitives

에이전트와 React 애플리케이션 간 **양방향 상태 공유**를 위한 핵심 hook 레퍼런스.

> v1 API 기준. v2에서는 `useAgent` / `useRenderToolCall`로 마이그레이션 권장.

---

## 개요

Shared State는 에이전트의 실행 상태를 UI에 실시간 반영하고, 사용자가 UI에서 변경한 값을 에이전트 실행에 즉시 전달하는 메커니즘이다.

- 에이전트 진행 상황 및 중간 결과를 UI에 표시
- UI 인터랙션으로 에이전트 상태 업데이트
- 양방향 동기화: 에이전트 출력 -> UI 반영, UI 입력 -> 에이전트 반영

---

## useCoAgent

에이전트를 애플리케이션에 통합하고, 상태를 양방향으로 읽기/쓰기할 수 있는 hook.

### Parameters (`UseCoagentOptions`)

| Parameter | Type | Required | 설명 |
|-----------|------|----------|------|
| `name` | `string` | Yes | 에이전트 식별자 |
| `initialState` | `T` | No | 초기 상태 객체 |
| `state` | `T` | No | 외부 상태 관리 시 사용 (controlled) |
| `setState` | `(state: T) => void` | No | 외부 상태 업데이트 함수 |

### Return Values

| Property | Type | 설명 |
|----------|------|------|
| `state` | `T` | 현재 에이전트 상태 (reactive) |
| `setState` | `(state: T) => void` | 상태 업데이트 함수 |
| `running` | `boolean` | 에이전트 실행 중 여부 |
| `start` | `() => void` | 에이전트 시작 |
| `stop` | `() => void` | 에이전트 중지 |
| `run` | `() => void` | 에이전트 실행 |
| `name` | `string` | 에이전트 이름 |
| `nodeName` | `string` | 현재 실행 노드 이름 |

### 사용 예시

```tsx
import { useCoAgent } from "@copilotkit/react-core";

interface AgentState {
  language: string;
  results: string[];
}

function MyComponent() {
  const { state, setState, running, run, stop } = useCoAgent<AgentState>({
    name: "sample_agent",
    initialState: {
      language: "ko",
      results: [],
    },
  });

  return (
    <div>
      <p>Status: {running ? "실행 중" : "대기"}</p>
      <p>Language: {state.language}</p>

      {/* UI에서 에이전트 상태 변경 */}
      <button onClick={() => setState({ ...state, language: "en" })}>
        Switch to English
      </button>

      <button onClick={run}>실행</button>
      <button onClick={stop}>중지</button>

      <ul>
        {state.results.map((r, i) => (
          <li key={i}>{r}</li>
        ))}
      </ul>
    </div>
  );
}
```

### v2 마이그레이션 (`useAgent`)

```tsx
import { useAgent } from "@copilotkit/react-core/v2";

function MyComponent() {
  const { agent } = useAgent({ agentId: "sample_agent" });

  // 상태 읽기 (reactive - 에이전트 상태 변경 시 자동 업데이트)
  const language = agent.state?.language;

  // 상태 쓰기
  agent.setState({ language: "en" });

  // 재실행
  agent.runAgent();
}
```

---

## useCoAgentStateRender

에이전트 상태를 **채팅 UI 내에서** 렌더링하는 hook. 중간 진행 상황이나 실시간 결과를 채팅 메시지로 표시할 때 사용한다.

### Parameters

| Parameter | Type | Required | 설명 |
|-----------|------|----------|------|
| `name` | `string` | Yes | 대상 CoAgent 이름 |
| `nodeName` | `string` | No | 특정 노드만 타겟팅 |
| `render` | `(info: RenderInfo<T>) => ReactNode \| string \| void` | Yes | 상태 기반 렌더링 함수 |

### RenderInfo 객체

| Property | Type | 설명 |
|----------|------|------|
| `state` | `T` | 현재 에이전트 상태 |
| `nodeName` | `string` | 현재 실행 노드 |
| `status` | `string` | 실행 상태 |

### 사용 예시

```tsx
import { useCoAgentStateRender } from "@copilotkit/react-core";

interface SearchState {
  query: string;
  sources: string[];
  answer: string;
}

function SearchProgress() {
  useCoAgentStateRender<SearchState>({
    name: "search_agent",
    render: ({ state, nodeName, status }) => {
      // 검색 진행 상황을 채팅에 표시
      if (nodeName === "searching") {
        return (
          <div>
            <p>검색 중: {state.query}</p>
            <p>발견된 소스: {state.sources.length}개</p>
          </div>
        );
      }

      if (nodeName === "summarizing") {
        return <p>결과 요약 중...</p>;
      }

      return null;
    },
  });

  return null; // UI는 채팅 내에서 렌더링됨
}
```

### 특정 노드만 렌더링

```tsx
useCoAgentStateRender<SearchState>({
  name: "search_agent",
  nodeName: "searching", // 이 노드 실행 시에만 렌더링
  render: ({ state }) => (
    <div className="search-progress">
      <Spinner /> {state.sources.length}개 소스 검색 완료
    </div>
  ),
});
```

### v2 마이그레이션 (`useRenderToolCall`)

v2에서는 `useRenderToolCall`을 사용하여 동일한 기능을 구현한다.

---

## Python 에이전트 상태 정의 (LangGraph)

프론트엔드 hook과 연동하려면 Python 에이전트에서 상태를 정의해야 한다.

```python
from copilotkit import CopilotKitState

class AgentState(CopilotKitState):
    language: str = "ko"
    results: list[str] = []
```

TypeScript 에이전트의 경우:

```typescript
import { CopilotKitStateAnnotation } from "@copilotkit/sdk";

const AgentState = CopilotKitStateAnnotation.extend({
  language: { value: "ko" },
  results: { value: [] },
});
```

---

원본: https://docs.copilotkit.ai/coagents/shared-state/primitives
