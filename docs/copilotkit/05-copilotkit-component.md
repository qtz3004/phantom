# CopilotKit Provider Component

애플리케이션 전체에 Copilot 기능을 활성화하는 **최상위 Provider 컴포넌트**.

> v1, v2 API 모두 호환. `@copilotkit/react-core`에서 import (v2 서브패키지 아님).

---

## 설치

```bash
npm install @copilotkit/react-core @copilotkit/react-ui
```

## 기본 사용법

```tsx
import { CopilotKit } from "@copilotkit/react-core";
import "@copilotkit/react-ui/styles.css";

function App() {
  return (
    <CopilotKit
      runtimeUrl="/api/copilotkit"
      agent="my_agent"
    >
      <YourApp />
    </CopilotKit>
  );
}
```

### Cloud 사용 시

```tsx
<CopilotKit publicApiKey="ck_pub_..." agent="my_agent">
  <YourApp />
</CopilotKit>
```

---

## Props

### 인증 및 설정

| Prop | Type | Required | 설명 |
|------|------|----------|------|
| `publicApiKey` | `string` | No | Copilot Cloud API 키 (cloud.copilotkit.ai에서 발급) |
| `publicLicenseKey` | `string` | No | 프리미엄 기능용 라이선스 키 |
| `runtimeUrl` | `string` | No | 자체 호스팅 Copilot Runtime endpoint URL |
| `agent` | `string` | No | 사용할 에이전트 이름 |
| `threadId` | `string` | No | 대화 thread 식별자 |
| `children` | `ReactNode` | **Yes** | Provider 내부에 렌더링할 컨텐츠 |

### HTTP 요청 설정

| Prop | Type | Default | 설명 |
|------|------|---------|------|
| `headers` | `Record<string, string>` | `{}` | 추가 HTTP 헤더 (인증 토큰 등) |
| `credentials` | `RequestCredentials` | - | cross-origin 요청 시 쿠키 처리 (`include`, `same-origin` 등) |
| `properties` | `Record<string, any>` | `{}` | 커스텀 속성 (`user_id`, `threadMetadata`, LangGraph 인증 등) |

### 서비스 Endpoint

| Prop | Type | 설명 |
|------|------|------|
| `transcribeAudioUrl` | `string` | 음성 전사 서비스 URL |
| `textToSpeechUrl` | `string` | 텍스트 음성 변환 서비스 URL |

### 기능 설정

| Prop | Type | Default | 설명 |
|------|------|---------|------|
| `showDevConsole` | `boolean` | `false` | 에러 배너 및 토스트 표시 |
| `enableInspector` | `boolean` | `false` | AG-UI Inspector 활성화 |
| `forwardedParameters` | `{ temperature?: number }` | - | 태스크 실행 시 전달할 파라미터 |

### 안전 및 인증

| Prop | Type | 설명 |
|------|------|------|
| `guardrails_c` | `{ validTopics?: string[], invalidTopics?: string[] }` | 토픽 기반 입력 제한 |
| `authConfig_c` | `{ SignInComponent: React.ComponentType }` | 인증 설정 (로그인 컴포넌트) |
| `onError` | `CopilotErrorHandler` | 에러 핸들러 (디버깅 컨텍스트 포함) |

### UI 설정

| Prop | Type | 설명 |
|------|------|------|
| `a2ui` | `{ theme?: Theme }` | Agent-to-UI 렌더러 테마 커스터마이징 |

---

## 실전 예시

### 인증 헤더 포함

```tsx
<CopilotKit
  runtimeUrl="/api/copilotkit"
  agent="my_agent"
  headers={{
    Authorization: `Bearer ${token}`,
  }}
  properties={{
    user_id: userId,
  }}
>
  <App />
</CopilotKit>
```

### 에러 핸들링

```tsx
<CopilotKit
  runtimeUrl="/api/copilotkit"
  onError={(error) => {
    console.error("CopilotKit error:", error);
    // 사용자에게 에러 알림
  }}
  showDevConsole={process.env.NODE_ENV === "development"}
>
  <App />
</CopilotKit>
```

### Guardrails 설정

```tsx
<CopilotKit
  runtimeUrl="/api/copilotkit"
  guardrails_c={{
    validTopics: ["coding", "documentation"],
    invalidTopics: ["politics", "personal"],
  }}
>
  <App />
</CopilotKit>
```

---

원본: https://docs.copilotkit.ai/reference/components/CopilotKit
