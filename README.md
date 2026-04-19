# Phantom

사내 Wiki(Confluence) 페이지를 에이전트로 지식화하여, 사용자의 자연어 질문에 관련 섹션만 골라 답변하는 DeepAgent 기반 프로젝트입니다. Wiki 원문을 LLM 친화적인 Markdown으로 구조화하고, 목차(h2 헤더)만으로 사용자 질문과 시맨틱 매칭한 뒤 필요한 라인 범위만 읽어 답하기 때문에 토큰 사용량이 크게 줄어듭니다.

> **브랜치**: https://github.com/qtz3004/phantom/tree/demo-03

## 사전 준비

의존성 설치와 `.env` 설정은 메인 브랜치의 안내를 따라 이미 완료된 상태를 전제로 합니다. 이 브랜치에서는 Wiki 페이지를 지식 소스로 등록하는 두 개의 슬래시 커맨드가 추가되었습니다.

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

knowledge_search 서브에이전트가 `tocs.md`의 h2 제목만 읽어 사용자 질문과 매칭되는 섹션을 고른 뒤, `knowledge.md`에서 해당 `라인: X-Y` 범위만 부분 read 하여 답변합니다. 전체 원문을 컨텍스트에 싣지 않기 때문에 토큰 사용량이 크게 줄어듭니다.
