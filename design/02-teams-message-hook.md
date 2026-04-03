# 02. Teams 메시지 후킹 설계

## 개요

Microsoft Teams에서 본인에게 수신되는 채팅 메시지를 로컬 FastAPI 서버로 실시간 전달받아 로깅하는 기능.
Azure Bot 대신 **Microsoft Graph API Change Notifications**(웹훅) 방식을 사용한다.

## 아키텍처

```
Teams 채팅 수신
  → Microsoft Graph (Change Notifications)
  → ngrok/devtunnel (HTTPS 터널)
  → localhost:8123/api/teams/notifications
  → 메시지 로깅
```

## Azure 설정

### 앱 등록 (Microsoft Entra ID)

| 항목 | 값 |
|------|-----|
| 이름 | `phantom-teams-hook` |
| 계정 유형 | 모든 조직 디렉터리의 계정 및 개인 Microsoft 계정 |
| 리디렉션 URI | `http://localhost:8123/api/teams/auth/callback` (Web) |

### API 권한 (Delegated)

본인 계정의 메시지만 수신하므로 **위임된 권한(Delegated permissions)** 사용.

| 권한 | 용도 |
|------|------|
| `Chat.Read` | 본인 채팅 메시지 읽기 |
| `User.Read` | 본인 프로필 조회 |

> 관리자 동의(Admin Consent)가 필요하지 않음 — 위임된 권한이므로 본인 동의만으로 충분.

### 인증 정보

```
teams/
├── credentials.yaml      # .gitignore 대상
└── credentials.example.yaml
```

```yaml
# credentials.yaml
teams:
  client_id: "앱 등록에서 발급받은 Application (client) ID"
  client_secret: "인증서 및 비밀에서 생성한 클라이언트 암호"
  tenant_id: "common"   # 개인 계정 포함 시 common 사용
  redirect_uri: "http://localhost:8123/api/teams/auth/callback"
```

## OAuth 2.0 인증 흐름

```
1. 브라우저에서 GET /api/teams/auth 접속
  → Microsoft 로그인 페이지로 리디렉트
  → 사용자 동의 후 authorization code 발급

2. GET /api/teams/auth/callback?code=xxx
  → authorization code → access_token + refresh_token 교환
  → 토큰을 메모리(또는 파일)에 저장

3. access_token으로 Graph API 구독 생성
```

### 토큰 관리

- `access_token` 만료: ~1시간 → `refresh_token`으로 자동 갱신
- 토큰 저장: 메모리 (서버 재시작 시 재로그인 필요)

## API 엔드포인트

### `GET /api/teams/auth`

Microsoft 로그인 페이지로 리디렉트. OAuth 인증 시작.

```
→ 302 Redirect to https://login.microsoftonline.com/common/oauth2/v2.0/authorize
    ?client_id={client_id}
    &response_type=code
    &redirect_uri={redirect_uri}
    &scope=Chat.Read User.Read
```

### `GET /api/teams/auth/callback`

OAuth 콜백. authorization code를 받아 토큰 교환 후 구독 생성.

```
← ?code=xxx
→ POST https://login.microsoftonline.com/common/oauth2/v2.0/token
→ access_token, refresh_token 저장
→ Graph API 구독 생성
→ 200 {"status": "authenticated", "subscription_id": "..."}
```

### `POST /api/teams/notifications`

Graph API 웹훅 수신 엔드포인트. 두 가지 역할을 수행한다.

**1) 구독 검증 (Validation)**

Graph API가 구독 생성 시 validationToken 파라미터로 검증 요청을 보낸다.

```
← POST /api/teams/notifications?validationToken=xxx
→ 200 text/plain: xxx (validationToken 값 그대로 반환)
```

**2) 메시지 알림 수신**

```json
← POST /api/teams/notifications
{
  "value": [
    {
      "subscriptionId": "...",
      "changeType": "created",
      "resource": "chats/{chat-id}/messages/{message-id}",
      "resourceData": { "@odata.id": "..." }
    }
  ]
}
→ 202 Accepted
→ resource URL로 Graph API 호출하여 메시지 본문 조회
→ 로깅
```

## Graph API 구독

### 구독 생성

```http
POST https://graph.microsoft.com/v1.0/subscriptions
Authorization: Bearer {access_token}

{
  "changeType": "created",
  "notificationUrl": "https://{터널URL}/api/teams/notifications",
  "resource": "/me/chats/getAllMessages",
  "expirationDateTime": "{현재시각 + 60분}",
  "clientState": "{랜덤 검증용 문자열}"
}
```

### 구독 갱신

구독 만료 전(60분) 자동 갱신. 백그라운드 타이머로 50분마다 갱신 요청.

```http
PATCH https://graph.microsoft.com/v1.0/subscriptions/{subscription-id}
Authorization: Bearer {access_token}

{
  "expirationDateTime": "{현재시각 + 60분}"
}
```

## 메시지 로깅

### 로그 포맷

```
[Teams] 2026-04-03 14:32:15 | 채팅: {chat_id} | 발신자: 홍길동 (hong@company.com) | 메시지: 안녕하세요, 회의 시간 변경 건입니다.
```

### 로거 설정

기존 `golden-cabbage` 로거와 별도로 `teams-hook` 로거 사용.

```python
logger = logging.getLogger("teams-hook")
```

### 로그 출력

- 콘솔 출력 (stdout)
- 향후 확장: 파일 저장, DB 저장, 에이전트 연동

## 파일 구조

```
phantom/
├── server.py                    # 기존 서버 — teams 라우터 include
├── teams/
│   ├── __init__.py
│   ├── router.py                # FastAPI APIRouter (3개 엔드포인트)
│   ├── auth.py                  # OAuth 토큰 관리 (발급, 갱신, 저장)
│   ├── subscription.py          # Graph API 구독 생성/갱신/삭제
│   ├── handler.py               # 알림 수신 → 메시지 조회 → 로깅
│   ├── credentials.yaml         # .gitignore 대상
│   └── credentials.example.yaml
```

### server.py 변경

```python
from teams.router import teams_router

app.include_router(teams_router, prefix="/api/teams")
```

## 처리 흐름

```
서버 시작
  → GET /api/teams/auth (브라우저에서 1회)
  → Microsoft 로그인 + 동의
  → GET /api/teams/auth/callback
  → access_token 확보
  → Graph API 구독 생성 (notificationUrl = 터널 HTTPS URL)
  → 구독 검증 (POST /api/teams/notifications?validationToken=xxx)
  → 구독 활성화

Teams 메시지 수신 시:
  → Graph → POST /api/teams/notifications (알림)
  → handler: resource URL로 메시지 본문 GET 요청
  → 발신자, 시간, 내용 파싱
  → 로거 출력
```

## 사전 준비

- [ ] Azure 앱 등록 완료 (client_id, client_secret 확보)
- [ ] `credentials.yaml` 작성
- [ ] ngrok 또는 devtunnel 설치
- [ ] `.gitignore`에 `teams/credentials.yaml` 추가

## 미결정 사항

- [ ] 로그 파일 저장 여부 (현재는 콘솔 출력만)
- [ ] 메시지 수신 시 에이전트 자동 응답 연동 여부
- [ ] 터널 URL 변경 시 구독 재생성 자동화 여부
- [ ] 서버 재시작 시 재인증 UX (토큰 파일 저장으로 전환 여부)
