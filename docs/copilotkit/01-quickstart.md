# CopilotKit Quickstart

CopilotKit으로 AI 에이전트 애플리케이션을 빠르게 시작하는 가이드.

## CLI로 시작하기

```bash
npx copilotkit@latest create
```

## Built-in Agent 방식 (가장 간단)

### 사전 요구사항

- OpenAI API key (또는 Anthropic/Google)
- Node.js 20+

### 1. 프로젝트 생성

```bash
npx create-next-app@latest my-copilot-app
cd my-copilot-app
```

### 2. 패키지 설치

```bash
npm install @copilotkit/react-core @copilotkit/react-ui @copilotkit/runtime
```

### 3. 환경 변수 설정

```plaintext title=".env"
OPENAI_API_KEY=your_openai_api_key
```

### 4. Copilot Runtime API Route 생성

```ts title="app/api/copilotkit/route.ts"
import {
  CopilotRuntime,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { BuiltInAgent } from "@copilotkit/runtime/v2";
import { NextRequest } from "next/server";

const builtInAgent = new BuiltInAgent({
  model: "openai:gpt-5.2",
});

const runtime = new CopilotRuntime({
  agents: { default: builtInAgent },
});

export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};
```

### 5. CopilotKit Provider 설정

```tsx title="app/layout.tsx"
import { CopilotKit } from "@copilotkit/react-core";
import "@copilotkit/react-ui/v2/styles.css";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <CopilotKit runtimeUrl="/api/copilotkit">
          {children}
        </CopilotKit>
      </body>
    </html>
  );
}
```

### 6. Chat UI 추가

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

### 7. 개발 서버 시작

```bash
npm run dev
```

## 핵심 구조 요약

| 구성 요소 | 역할 |
|-----------|------|
| `@copilotkit/runtime` | 백엔드 런타임 (API route) |
| `@copilotkit/react-core` | React Provider 및 hooks |
| `@copilotkit/react-ui` | 사전 빌드된 UI 컴포넌트 |
| `BuiltInAgent` | CopilotKit 기본 에이전트 |
| `CopilotRuntime` | 에이전트 라우팅 및 미들웨어 관리 |
| `<CopilotKit>` | 프론트엔드 Provider 컴포넌트 |
| `<CopilotSidebar>` | 사이드바 채팅 UI (Popup, Chat도 가능) |

## 다음 단계

- **Server Tools**: 에이전트에 백엔드 도구 제공
- **MCP Servers**: MCP 서버 연결로 도구 확장
- **Model Selection**: Anthropic, Google 등 다른 모델 사용
- **Frontend Tools**: 에이전트가 UI와 상호작용

---

원본: https://docs.copilotkit.ai/quickstart
