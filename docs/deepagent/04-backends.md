# Backends

Deep Agents는 플러그 가능한 백엔드를 통해 파일시스템 작업을 노출합니다. `ls`, `read_file`, `write_file`, `edit_file`, `glob`, `grep` 도구를 포함합니다.

## 내장 백엔드

### StateBackend (임시)

```python
from deepagents.backends import StateBackend

agent = create_deep_agent(
    backend=(lambda rt: StateBackend(rt))
)
```

LangGraph 에이전트 상태에 파일 저장. 현재 스레드 내에서만 유지. 스크래치 패드와 중간 결과에 적합.

### FilesystemBackend (로컬 디스크)

```python
from deepagents.backends import FilesystemBackend

agent = create_deep_agent(
    backend=FilesystemBackend(root_dir=".", virtual_mode=True)
)
```

실제 파일을 설정 가능한 루트 디렉토리 아래에서 읽기/쓰기. `virtual_mode=True`로 경로를 샌드박싱.

> **보안 경고**: 직접 파일시스템 접근 권한 부여. 개발 또는 통제된 CI/CD 환경에서만 사용.

### LocalShellBackend (로컬 셸)

```python
from deepagents.backends import LocalShellBackend

agent = create_deep_agent(
    backend=LocalShellBackend(root_dir=".", env={"PATH": "/usr/bin:/bin"})
)
```

FilesystemBackend를 확장하여 `execute` 도구로 셸 명령 실행. `timeout` (기본 120초), `max_output_bytes` (기본 100,000) 지원.

> **경고**: 제한 없는 셸 실행 권한 부여. 신뢰할 수 있는 개발 환경에서만 사용.

### StoreBackend (LangGraph Store)

```python
from langgraph.store.memory import InMemoryStore
from deepagents.backends import StoreBackend

agent = create_deep_agent(
    backend=lambda rt: StoreBackend(
        rt,
        namespace=lambda ctx: (ctx.runtime.context.user_id,),
    ),
    store=InMemoryStore()
)
```

LangGraph `BaseStore`에 파일 저장. 스레드 간 지속적 저장소.

#### Namespace Factories

```python
# 사용자별 격리
backend = lambda rt: StoreBackend(rt, namespace=lambda ctx: (ctx.runtime.context.user_id,))

# 어시스턴트별 (공유 저장소)
backend = lambda rt: StoreBackend(rt, namespace=lambda ctx: (get_config()["metadata"]["assistant_id"],))

# 스레드별 스코핑
backend = lambda rt: StoreBackend(rt, namespace=lambda ctx: (get_config()["configurable"]["thread_id"],))
```

### CompositeBackend (라우터)

```python
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend

composite_backend = lambda rt: CompositeBackend(
    default=StateBackend(rt),
    routes={
        "/memories/": StoreBackend(rt),
    }
)

agent = create_deep_agent(
    backend=composite_backend,
    store=InMemoryStore()
)
```

경로 프리픽스 기반으로 다른 백엔드로 라우팅. 더 긴 프리픽스가 우선.

## 커스텀 백엔드

### BackendProtocol 구현

필수 메서드:
- `ls_info(path) -> list[FileInfo]`
- `read(file_path, offset, limit) -> str`
- `grep_raw(pattern, path, glob) -> list[GrepMatch] | str`
- `glob_info(pattern, path) -> list[FileInfo]`
- `write(file_path, content) -> WriteResult`
- `edit(file_path, old_string, new_string, replace_all) -> EditResult`

### S3 Backend 예제

```python
from deepagents.backends.protocol import BackendProtocol, WriteResult, EditResult

class S3Backend(BackendProtocol):
    def __init__(self, bucket: str, prefix: str = ""):
        self.bucket = bucket
        self.prefix = prefix.rstrip("/")

    def ls_info(self, path): ...
    def read(self, file_path, offset=0, limit=2000): ...
    def grep_raw(self, pattern, path=None, glob=None): ...
    def glob_info(self, pattern, path="/"): ...
    def write(self, file_path, content): ...
    def edit(self, file_path, old_string, new_string, replace_all=False): ...
```

## 정책 적용 (Policy Enforcement)

```python
class GuardedBackend(FilesystemBackend):
    def __init__(self, *, deny_prefixes: list[str], **kwargs):
        super().__init__(**kwargs)
        self.deny_prefixes = [p if p.endswith("/") else p + "/" for p in deny_prefixes]

    def write(self, file_path, content):
        if any(file_path.startswith(p) for p in self.deny_prefixes):
            return WriteResult(error=f"Writes not allowed under {file_path}")
        return super().write(file_path, content)
```

## 라우팅 예제

```python
composite_backend = lambda rt: CompositeBackend(
    default=StateBackend(rt),
    routes={
        "/memories/": FilesystemBackend(root_dir="/deepagents/myagent", virtual_mode=True),
    },
)
```

- `/workspace/plan.md` → StateBackend (임시)
- `/memories/agent.md` → FilesystemBackend (영구)

> 원본: https://docs.langchain.com/oss/python/deepagents/backends
