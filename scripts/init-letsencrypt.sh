#!/bin/bash
# Let's Encrypt 초기 인증서 발급 스크립트
# 최초 1회만 실행하면 됩니다. 이후 갱신은 certbot 컨테이너가 자동 처리합니다.

set -e

DOMAIN="phantom-agent.duckdns.org"
EMAIL=""  # 갱신 알림 이메일 (선택)
COMPOSE="docker compose"

echo "=== Let's Encrypt 초기 인증서 발급 ==="

# 1. 기존 컨테이너 정리
echo "[1/5] 기존 컨테이너 정리..."
$COMPOSE down 2>/dev/null || true

# 2. 임시 자체 서명 인증서 생성 (nginx 기동용)
echo "[2/5] 임시 인증서 생성..."
$COMPOSE run --rm --entrypoint "" certbot sh -c "
  mkdir -p /etc/letsencrypt/live/$DOMAIN
  if [ ! -f /etc/letsencrypt/live/$DOMAIN/fullchain.pem ]; then
    openssl req -x509 -nodes -newkey rsa:2048 -days 1 \
      -keyout /etc/letsencrypt/live/$DOMAIN/privkey.pem \
      -out /etc/letsencrypt/live/$DOMAIN/fullchain.pem \
      -subj '/CN=$DOMAIN'
    echo '임시 인증서 생성 완료'
  else
    echo '인증서가 이미 존재합니다'
  fi
"

# 3. nginx 시작 (임시 인증서로)
echo "[3/5] Nginx 시작..."
$COMPOSE up -d nginx

# 4. 임시 인증서 삭제 후 실제 인증서 발급
echo "[4/5] Let's Encrypt 인증서 발급 중..."
$COMPOSE run --rm --entrypoint "" certbot sh -c "
  rm -rf /etc/letsencrypt/live/$DOMAIN
  rm -rf /etc/letsencrypt/archive/$DOMAIN
  rm -rf /etc/letsencrypt/renewal/$DOMAIN.conf
"

EMAIL_ARG=""
if [ -n "$EMAIL" ]; then
  EMAIL_ARG="--email $EMAIL"
else
  EMAIL_ARG="--register-unsafely-without-email"
fi

$COMPOSE run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  $EMAIL_ARG \
  --agree-tos \
  --no-eff-email \
  -d $DOMAIN

# 5. nginx 재시작 (실제 인증서 적용)
echo "[5/5] Nginx 재시작..."
$COMPOSE exec nginx nginx -s reload

echo ""
echo "=== 완료! ==="
echo "인증서 발급 성공: $DOMAIN"
echo "전체 서비스 시작: docker compose up -d"
