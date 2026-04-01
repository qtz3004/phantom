# Skills

스킬은 재사용 가능한 에이전트 기능으로 특화된 워크플로우와 도메인 지식을 제공합니다.

## 스킬 구조

```
skills/
├── langgraph-docs
│   └── SKILL.md
└── arxiv_search
    ├── SKILL.md
    └── arxiv_search.py
```

### SKILL.md 형식

```markdown
---
name: langgraph-docs
description: Use this skill for requests related to LangGraph
license: MIT
compatibility: Requires internet access
metadata:
  author: langchain
  version: "1.0"
allowed-tools: fetch_url
---

# langgraph-docs

## Instructions

1. Fetch the Documentation Index
2. Select Relevant Documentation
3. Fetch Selected Documentation
4. Provide Accurate Guidance
```

## 작동 방식

1. **Match**: 사용자 프롬프트 도착 시 스킬 description과 매칭
2. **Read**: 매칭되면 전체 `SKILL.md` 파일 읽기
3. **Execute**: 스킬 지침 따라 실행

> 점진적 공개(progressive disclosure) - 필요할 때만 스킬 정보 로드

## 사용법

```python
agent = create_deep_agent(
    skills=["/skills/"],
    checkpointer=checkpointer,
)

# StateBackend: invoke 시 files로 스킬 파일 전달
result = agent.invoke(
    {"messages": [...], "files": skills_files},
    config={"configurable": {"thread_id": "12345"}},
)

# FilesystemBackend: 디스크에서 직접 로드
agent = create_deep_agent(
    backend=FilesystemBackend(root_dir="/project"),
    skills=["/project/skills/"],
)
```

## 서브에이전트 스킬

- **General-purpose subagent**: 메인 에이전트 스킬 자동 상속
- **Custom subagents**: 스킬 상속 안함. 별도 `skills` 매개변수 사용

```python
research_subagent = {
    "name": "researcher",
    "skills": ["/skills/research/", "/skills/web-search/"],
}

agent = create_deep_agent(
    skills=["/skills/main/"],
    subagents=[research_subagent],
)
```

## 소스 우선순위

`skills` 배열에서 나중에 나열된 소스가 우선 (last wins).

```python
agent = create_deep_agent(
    skills=["/skills/user/", "/skills/project/"],  # project이 우선
)
```

## Skills vs. Memory

| 측면 | Skills | Memory |
|------|--------|--------|
| 목적 | 온디맨드 기능 | 항상 로드되는 영구 컨텍스트 |
| 로딩 | 관련성 판단 시에만 | 시작 시 항상 주입 |
| 형식 | `SKILL.md` | `AGENTS.md` |
| 사용 시기 | 작업별 대용량 지침 | 항상 관련된 컨텍스트 |

> 원본: https://docs.langchain.com/oss/python/deepagents/skills
