# Phantom

사내 Wiki(Confluence) 페이지를 에이전트로 지식화하여, 사용자의 자연어 질문에 관련 섹션만 골라 답변하는 DeepAgent 기반 프로젝트입니다. Wiki 원문을 LLM 친화적인 Markdown으로 구조화하고, 목차(h2 헤더)만으로 사용자 질문과 시맨틱 매칭한 뒤 필요한 라인 범위만 읽어 답하기 때문에 토큰 사용량이 크게 줄어듭니다.

> **브랜치**: https://github.com/qtz3004/phantom/tree/demo-03

## 이 프로젝트의 목적

**사내 위키 정보를 LLM에 학습시키지 않고도** 그 내용으로 답하는 에이전트를 만들어 봅니다. LLM 단독으로는 답할 수 없는 "사내 정책 문서 제3조에 뭐라고 적혀 있어?" 같은 질문을 — 모델이 도구를 호출해 위키에서 가져온 실제 본문을 인용해 답하도록 만드는 것이 이 실습의 목표입니다.

핵심은 **컨텍스트(토큰) 절약** 입니다. 위키 문서를 통째로 매 호출마다 LLM에 밀어 넣으면 비싸고 느리고 정확도도 떨어집니다. 대신:

> 💡 **팁 — "헤더만 LLM, 본문은 미들웨어"**
>
> - LLM에게는 문서의 **목차(h2 헤더 라인) 만** 보여줍니다. 예: `## 제3조 보안정책 | 라인: 42-58`
> - LLM은 *"42-58 라인이 필요해"* 처럼 **라인 범위만 지목**합니다.
> - **미들웨어(파이썬 소스)** 가 실제 파일에서 그 라인들을 잘라 도구 결과로 끼워 넣습니다.
> - 결과: LLM 프롬프트에는 매번 목차 한 화면 + 필요한 본문 몇 줄만 들어가고, 전체 문서는 디스크에 둔 채 정확하게 인용할 수 있습니다.

이 방식이 "단순히 RAG로 위키를 통째로 임베딩" 하는 접근보다 결정론적이고, 검증 가능하며, 토큰 비용을 한 자릿수로 줄여 줍니다.

> 핵심 한 줄: **"LLM은 목차만 본다. 본문은 코드가 정확한 라인으로 가져와 넘긴다."**

## 사전 준비

초기 세팅(uv 설치, 프로젝트 클론, `.env` 작성, Claude Code 실행 등)은 [`main` 브랜치 README](https://github.com/qtz3004/phantom/blob/main/README.md) 의 *사전 준비* 와 *시작하기* 단계를 먼저 마쳐 주세요. 이 브랜치는 그 위에 Wiki 페이지를 지식 소스로 등록하는 두 개의 슬래시 커맨드가 추가된 상태를 전제로 합니다.

아래 명령으로 이 브랜치로 전환해 주세요.

```bash
git fetch origin
git checkout demo-03
```

Confluence 접근을 위해 `.claude/skills/wiki-crawler/credentials.yaml` 파일을 생성하고 **본인의 사내 계정 정보**를 입력해 주세요. 예시 파일이 같은 디렉터리에 `credentials.example.yaml`로 준비되어 있습니다.

```yaml
wiki:
  base_url: https://konawiki.konai.com
  username: your-id       # 사내 Wiki 로그인 ID
  password: your-password # 사내 Wiki 로그인 비밀번호
```

`credentials.yaml`은 `.gitignore`에 등록되어 있어 커밋되지 않습니다.

## 시작하기

### 1. `/wiki-crawler`로 원문 생성

```
/wiki-crawler
https://konawiki.konai.com/display/.../페이지제목
```

스킬이 Confluence REST API로 본문과 첨부를 가져와 `.claude/skills/wiki-crawler/output/{pageId}.md`를 생성합니다. 각 섹션은 sample.md 구조(`## 뉴스형 h2 제목 | 라인: X-Y | 참조: A-B`)를 따릅니다.

Wiki 페이지 형태는 서술형 문서, 거대한 단일 표, 컴포넌트 카탈로그 등 다양하기 때문에 자동 생성 결과가 항상 원하는 형태가 아닐 수 있습니다. 이런 경우 Claude에게 대화로 맥락을 전달하며 직접 편집을 지시해 주세요.

- "이 페이지는 컴포넌트명으로 질의할 거야. 지금은 표 한 덩어리인데 각 행을 개별 h2 섹션으로 쪼개줘."
- "h2 제목이 너무 축약돼 있어서 검색이 안 될 것 같아. 한 줄 요약을 붙인 서술형으로 다시 써."
- "이 원문은 FAQ 형식이야. 질문-답변 쌍마다 h2를 만들고 질문문을 제목으로 써."
- "sample.md 구조랑 비교해서 어긋난 부분 알려주고 고쳐줘."

기준은 하나입니다. **출력 파일의 h2 라인만 훑어서 사용자 질문에 매칭되는 섹션을 고를 수 있는가?** 그렇지 않다면 통과할 때까지 대화로 수정하시면 됩니다.

### 2. `/header-extractor`로 배포

```
/header-extractor
.claude/skills/wiki-crawler/output/{pageId}.md
```

1단계 결과 파일 경로를 입력하시면 스킬이 다음을 수행합니다.

- 파일명 참조를 `knowledge.md`로 일괄 치환한 원문을 `subagents/knowledge_search/docs/knowledge.md`에 덮어씁니다.
- 헤더와 `> 출처` / `> 첨부` 메타만 뽑아 `subagents/knowledge_search/docs/tocs.md`에 덮어씁니다.

이 단계는 기계적 변환이라 거의 실패하지 않습니다. 1단계 결과가 sample.md 구조만 지킨다면 Claude는 결과 확인만 하면 됩니다.

### 3. 질문

이제 자연어로 물어보면 됩니다 — `knowledge_search` 서브에이전트가 위 *이 프로젝트의 목적* 에서 설명한 "헤더만 LLM → 라인 범위만 미들웨어로" 흐름으로 답합니다.
