# CopilotChat Component

에이전트를 채팅 뷰에 연결하는 **고수준 채팅 UI 컴포넌트**.

> v1 `CopilotChat`은 유지되지만 v2 API의 `CopilotChat`으로 마이그레이션 권장.

---

## 설치

```bash
npm install @copilotkit/react-core @copilotkit/react-ui
```

```tsx
import "@copilotkit/react-ui/styles.css"; // 기본 스타일 필수
```

---

## 기본 사용법

```tsx
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

function App() {
  return (
    <CopilotKit runtimeUrl="/api/copilotkit" agent="my_agent">
      <CopilotChat
        labels={{ chatInputPlaceholder: "무엇이든 물어보세요..." }}
      />
    </CopilotKit>
  );
}
```

---

## 관련 컴포넌트

| 컴포넌트 | 설명 |
|----------|------|
| `CopilotChat` | 인라인 채팅 패널 |
| `CopilotPopup` | 플로팅 팝업 패널 |
| `CopilotSidebar` | 고정 사이드 패널 |
| `CopilotChatView` | 트랜스크립트 + 입력 레이아웃 |
| `CopilotChatMessageView` | 메시지 목록 렌더링 |
| `CopilotChatInput` | 텍스트 입력 컨트롤 |

---

## Props

### 고유 Props

| Prop | Type | Default | 설명 |
|------|------|---------|------|
| `agentId` | `string` | - | `CopilotKit` Provider에 설정된 에이전트 ID |
| `threadId` | `string` | - | 기존 대화 이어가기 위한 thread ID |
| `labels` | `Partial<CopilotChatLabels>` | - | 텍스트 커스터마이징 |
| `chatView` | `SlotValue` | - | 내부 `CopilotChatView` slot override |
| `onError` | `(error: Error) => void` | - | 채팅 에이전트 전용 에러 핸들러 |
| `isModalDefaultOpen` | `boolean` | - | Popup/Sidebar 초기 열림 상태 |

### CopilotChatView에서 상속

| Prop | Type | Default | 설명 |
|------|------|---------|------|
| `autoScroll` | `boolean` | `true` | 새 메시지 시 자동 스크롤 |
| `inputProps` | `object` | - | `CopilotChatInput` 추가 props |
| `welcomeScreen` | `ReactNode \| false` | - | 시작 화면 커스터마이징 |

### Labels 옵션

```tsx
<CopilotChat
  labels={{
    chatInputPlaceholder: "메시지를 입력하세요...",
    // 기타 텍스트 레이블
  }}
/>
```

### Suggestions 모드

3가지 suggestion 모드를 지원한다:

| 모드 | 설명 |
|------|------|
| `"auto"` | AI가 적절한 시점에 자동 생성 |
| `"manual"` | 프로그래밍으로 제어 |
| 정적 배열 | 고정 suggestion 목록 |

### Callbacks

| Callback | 설명 |
|----------|------|
| 메시지 전송 | 사용자 메시지 제출 시 |
| 생성 중지 | 응답 생성 중단 시 |
| 재생성 | 응답 재생성 시 |
| 복사 | 메시지 복사 시 |
| 피드백 | 좋아요/싫어요 클릭 시 |

---

## 실전 예시

### Popup 스타일

```tsx
import { CopilotPopup } from "@copilotkit/react-ui";

<CopilotKit runtimeUrl="/api/copilotkit" agent="my_agent">
  <CopilotPopup
    labels={{ chatInputPlaceholder: "AI에게 물어보기..." }}
    isModalDefaultOpen={false}
  />
</CopilotKit>
```

### Sidebar 스타일

```tsx
import { CopilotSidebar } from "@copilotkit/react-ui";

<CopilotKit runtimeUrl="/api/copilotkit" agent="my_agent">
  <CopilotSidebar>
    <YourApp />
  </CopilotSidebar>
</CopilotKit>
```

### Slot 시스템

Slot은 3가지 형태로 override 가능:

```tsx
// 1. 대체 컴포넌트
<CopilotChat chatView={<MyCustomChatView />} />

// 2. className 문자열
<CopilotChat chatView="my-custom-class" />

// 3. 부분 props 객체
<CopilotChat chatView={{ autoScroll: false }} />
```

### v2 API 사용

```tsx
import { CopilotChat } from "@copilotkit/react-ui/v2";

<CopilotChat
  agentId="my_agent"
  labels={{ chatInputPlaceholder: "Ask me anything..." }}
/>
```

---

## 스타일 커스터마이징

기본 스타일시트를 import한 후 CSS로 override:

```tsx
import "@copilotkit/react-ui/styles.css";
```

커스텀 스타일은 별도 가이드 참조.

---

원본: https://docs.copilotkit.ai/reference/components/CopilotChat
