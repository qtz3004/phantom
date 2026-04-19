# Copilot Runtime

Copilot Runtime은 프론트엔드와 AI 에이전트를 연결하는 백엔드 레이어. 인증, 미들웨어, 라우팅 등을 제공한다.

## 기본 설정 (Next.js)

```ts title="app/api/copilotkit/route.ts"
import {
  CopilotRuntime,
  ExperimentalEmptyAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { NextRequest } from "next/server";

const serviceAdapter = new ExperimentalEmptyAdapter();

const runtime = new CopilotRuntime({
  agents: {
    // 에이전트 등록
  },
});

export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};
```

프론트엔드 연결:

```tsx
<CopilotKit runtimeUrl="/api/copilotkit">
  <YourApp />
</CopilotKit>
```

## Default Agent

`"default"` 이름으로 에이전트를 등록하면 프론트엔드에서 별도 설정 없이 자동으로 사용된다.

```ts
const runtime = new CopilotRuntime({
  agents: {
    "default": new HttpAgent({ url: "https://my-agent.example.com" }),
  },
});
```

여러 에이전트를 등록할 때, `"default"` 에이전트가 기본 채팅을 담당하고 다른 에이전트는 `useAgent` 또는 컴포넌트에 `agentId`를 전달하여 사용한다.

## Runtime이 제공하는 기능

### 인증 및 보안

Runtime은 서버에서 실행되므로 에이전트 통신이 서버사이드에서 이루어진다. API 키 보안 및 인증 검증에 유리하다.

### AG-UI Middleware

[AG-UI protocol](https://docs.copilotkit.ai/concepts/ag-ui-protocol)은 `agent.use` 미들웨어 레이어를 지원. 로깅, guardrails, request 변환 등을 서버사이드에서 실행한다.

### Agent Routing

여러 에이전트 등록 시, 자동으로 discovery 및 라우팅을 처리한다. 프론트엔드에서 각 에이전트의 위치를 알 필요 없다.

### Premium 기능

- **Threads**: 대화 지속성
- **Observability**: 모니터링
- **Inspector**: 디버깅

## Built-in Middleware

### A2UI

모든 에이전트에 `A2UIMiddleware`를 자동 적용:

```ts
const runtime = new CopilotRuntime({
  agents: { default: myAgent },
  a2ui: {},  // 모든 에이전트에 A2UI 활성화
});
```

특정 에이전트에만 적용:

```ts
a2ui: { agents: ["my-agent"] }
```

프론트엔드에서 커스텀 테마 적용:

```tsx
<CopilotKit runtimeUrl="/api/copilotkit" a2ui={{ theme: myCustomTheme }}>
  {children}
</CopilotKit>
```

### mcpApps

MCP 서버를 한 곳에서 설정:

```ts
const runtime = new CopilotRuntime({
  agents: { default: myAgent },
  mcpApps: {
    servers: [
      { type: "http", url: "http://localhost:3108/mcp", serverId: "my-server" },
    ],
  },
});
```

`agentId` 필드로 특정 에이전트에만 서버를 제한할 수 있다. 미지정 시 모든 에이전트에 적용.

## Runtime 없이 직접 연결 (개발용)

AG-UI 호환 에이전트에 직접 연결 가능. **프로덕션에서는 권장하지 않음.**

```tsx
import { HttpAgent } from "@ag-ui/client";

const myAgent = new HttpAgent({
  url: "https://my-agent.example.com",
});

<CopilotKit agents__unsafe_dev_only={{ "my-agent": myAgent }}>
  <YourApp />
</CopilotKit>
```

### Runtime vs 직접 연결 비교

| | Runtime 사용 | 직접 연결 |
|---|---|---|
| **인증** | 기본 제공 | 직접 구현 필요 |
| **AG-UI Middleware** | 서버사이드 실행 | 사용 불가 |
| **Agent Routing** | 자동 | 수동 |
| **Ecosystem 기능** | 전체 지원 | 제한적 |
| **공식 지원** | 지원됨 | 미지원 |
| **설정** | 백엔드 엔드포인트 필요 | 프론트엔드만 |

---

원본: https://docs.copilotkit.ai/concepts/copilot-runtime
