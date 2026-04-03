# CopilotKit Hooks

주요 React hook 레퍼런스.

---

## useCopilotChat

UI 없이 **프로그래밍 방식으로 채팅을 제어**하는 경량 headless hook.

> v1 API 기준. v2에서는 `useAgent`로 마이그레이션 권장.

### 주요 용도

- UI 표시 없이 프로그래밍으로 메시지 전송
- 프리빌트 컴포넌트를 코드로 제어
- 백그라운드 AI 작업 트리거
- Fire-and-forget 메시지 패턴

### Parameters

| Parameter | Type | Default | 설명 |
|-----------|------|---------|------|
| `id` | `string` | - | 고유 채팅 식별자. 같은 `id`를 공유하는 컴포넌트 간 상태 공유 |
| `headers` | `Record<string, string>` | - | 커스텀 HTTP 헤더 |
| `initialMessages` | `Message[]` | `[]` | 초기 메시지 목록 |
| `suggestions` | `"auto" \| "manual" \| string[]` | - | Suggestion 모드 |

### Return Values

| Property | Type | 설명 |
|----------|------|------|
| `appendMessage` | `(message: Message) => void` | 메시지 추가 |
| `reloadMessages` | `() => void` | 응답 재생성 |
| `stopGeneration` | `() => void` | 응답 생성 중단 |
| `reset` | `() => void` | 채팅 상태 초기화 |
| `isLoading` | `boolean` | 응답 생성 중 여부 |
| `runChatCompletion` | `() => void` | 채팅 완성 실행 (advanced) |

### 사용 예시

```tsx
import { useCopilotChat } from "@copilotkit/react-core";

function ChatController() {
  const {
    appendMessage,
    reloadMessages,
    stopGeneration,
    reset,
    isLoading,
  } = useCopilotChat({ id: "main-chat" });

  // 프로그래밍으로 메시지 전송
  const sendMessage = () => {
    appendMessage({
      role: "user",
      content: "오늘 할 일 목록을 만들어줘",
    });
  };

  return (
    <div>
      <button onClick={sendMessage}>메시지 전송</button>
      <button onClick={stopGeneration} disabled={!isLoading}>
        중지
      </button>
      <button onClick={reloadMessages}>재생성</button>
      <button onClick={reset}>초기화</button>
    </div>
  );
}
```

### 상태 공유 (같은 id)

```tsx
// 컴포넌트 A
const chatA = useCopilotChat({ id: "shared-chat" });

// 컴포넌트 B - 같은 id로 상태 공유
const chatB = useCopilotChat({ id: "shared-chat" });
// chatA.appendMessage() 호출 시 chatB에서도 반영됨
```

### 백그라운드 메시지 전송

```tsx
function BackgroundAI() {
  const { appendMessage } = useCopilotChat();

  useEffect(() => {
    // 페이지 로드 시 자동으로 AI에게 컨텍스트 전달
    appendMessage({
      role: "user",
      content: "사용자가 대시보드 페이지에 접속했습니다. 요약을 준비해주세요.",
    });
  }, []);

  return null; // headless - UI 없음
}
```

---

## useCopilotKit (v2)

CopilotKit core instance와 provider 수준 상태에 직접 접근하는 **저수준 hook**.

### Return Values

| Property | Type | 설명 |
|----------|------|------|
| `copilotkit` | `CopilotKitCore` | 에이전트, 도구, suggestion, 런타임 통신을 관리하는 중앙 인스턴스 |
| `executingToolCallIds` | `ReadonlySet<string>` | 현재 실행 중인 tool call ID 집합 |

### 주요 용도

```tsx
import { useCopilotKit } from "@copilotkit/react-core/v2";

function AdvancedControl() {
  const { copilotkit, executingToolCallIds } = useCopilotKit();

  // 등록된 에이전트 조회
  const agents = copilotkit.agents;

  // 런타임 연결 상태 구독
  copilotkit.onRuntimeConnectionStatusChanged((status) => {
    console.log("Runtime status:", status);
  });

  // 프로그래밍으로 도구 실행 (LLM 없이)
  copilotkit.runTool("my_tool", { param: "value" });

  // 실행 중인 tool call 모니터링
  const isExecuting = executingToolCallIds.size > 0;

  return <div>{isExecuting ? "도구 실행 중..." : "대기"}</div>;
}
```

### 주의사항

- `CopilotKitProvider` 바깥에서 사용하면 에러 발생
- `copilotkit` 인스턴스는 리렌더링 간 안정적 (stable reference)
- `executingToolCallIds`만 동적으로 변경
- 대부분의 경우 `useAgent`, `useFrontendTool` 등 고수준 hook 사용 권장

---

## 기타 주요 Hooks (v2)

| Hook | 설명 |
|------|------|
| `useAgent` | AG-UI 에이전트 인스턴스 접근 (v1 `useCoAgent` 대체) |
| `useFrontendTool` | 클라이언트 사이드 도구 핸들러 등록 |
| `useRenderTool` | 도구 호출에 대한 타입 안전 렌더러 등록 |
| `useAgentContext` | 에이전트에 동적 컨텍스트 제공 |
| `useSuggestions` | 채팅 suggestion 접근 |
| `useCopilotChatConfiguration` | 채팅 설정 접근 |

---

원본: https://docs.copilotkit.ai/reference/hooks/useCopilotChat
