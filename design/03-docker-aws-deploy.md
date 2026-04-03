# 03. Docker + AWS EC2 배포 가이드

## 개요

Phantom 백엔드(FastAPI) + 프론트엔드(Next.js)를 Docker Compose로 패키징하여
AWS EC2 t2.micro (무료 티어)에 배포한다.

## 아키텍처

```
EC2 t2.micro (1vCPU, 1GB RAM)
├── docker-compose
│   ├── backend  (FastAPI, port 8123)
│   └── frontend (Next.js, port 3000)
└── .env (API 키)
```

## 로컬 빌드 및 테스트

```bash
# .env 파일 준비
cp .env.example .env
# GOOGLE_API_KEY, TAVILY_API_KEY 입력

# 빌드 및 실행
docker compose up --build

# 확인
curl http://localhost:8123/health
open http://localhost:3000
```

## EC2 배포 절차

### 1. EC2 인스턴스 생성

- **AMI**: Amazon Linux 2023
- **인스턴스 유형**: t2.micro (무료 티어)
- **보안 그룹**: 인바운드 포트 3000, 8123, 22(SSH) 허용
- **키 페어**: 생성 후 `.pem` 파일 보관

### 2. Docker 설치

```bash
ssh -i your-key.pem ec2-user@<EC2-IP>

sudo yum update -y
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user

# docker compose plugin
sudo mkdir -p /usr/local/lib/docker/cli-plugins
sudo curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
  -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

# 재접속 (그룹 반영)
exit
ssh -i your-key.pem ec2-user@<EC2-IP>
```

### 3. 코드 배포

```bash
# 방법 A: git clone
git clone https://github.com/<your-repo>/phantom.git
cd phantom

# 방법 B: 로컬에서 scp
scp -i your-key.pem -r . ec2-user@<EC2-IP>:~/phantom
```

### 4. 환경변수 설정

```bash
cp .env.example .env
vi .env
# GOOGLE_API_KEY=xxx
# TAVILY_API_KEY=xxx
```

### 5. 실행

```bash
docker compose up --build -d

# 로그 확인
docker compose logs -f

# 상태 확인
docker compose ps
```

### 6. 접속

```
http://<EC2-IP>:3000    # 프론트엔드
http://<EC2-IP>:8123    # 백엔드 API
```

## t2.micro 제약 사항

- **RAM 1GB**: 두 컨테이너 동시 실행 시 빡빡함. 스왑 추가 권장:
  ```bash
  sudo dd if=/dev/zero of=/swapfile bs=128M count=16  # 2GB 스왑
  sudo chmod 600 /swapfile
  sudo mkswap /swapfile
  sudo swapon /swapfile
  echo '/swapfile swap swap defaults 0 0' | sudo tee -a /etc/fstab
  ```
- **빌드는 로컬에서**: EC2에서 `docker compose build`는 메모리 부족 가능. 로컬 빌드 후 이미지 전송 권장:
  ```bash
  # 로컬에서
  docker compose build
  docker save phantom-backend phantom-frontend | gzip > images.tar.gz
  scp -i your-key.pem images.tar.gz ec2-user@<EC2-IP>:~/

  # EC2에서
  gunzip -c images.tar.gz | docker load
  docker compose up -d
  ```

## 파일 목록

| 파일 | 용도 |
|------|------|
| `Dockerfile` | 백엔드 이미지 (Python 3.12 + uv) |
| `frontend/Dockerfile` | 프론트엔드 이미지 (Node 22 + standalone) |
| `docker-compose.yml` | 두 서비스 오케스트레이션 |
| `.dockerignore` | 백엔드 빌드 제외 파일 |
| `frontend/.dockerignore` | 프론트엔드 빌드 제외 파일 |
