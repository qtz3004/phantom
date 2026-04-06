#!/bin/bash
# Let's Encrypt 인증서 발급 (DNS-01 + Duck DNS)
# 개인 와이파이에서 실행해야 합니다 (회사 프록시 우회)

set -e

DOMAIN="phantom-agent"
FQDN="${DOMAIN}.duckdns.org"
DUCKDNS_TOKEN="${DUCKDNS_TOKEN:?환경변수 DUCKDNS_TOKEN 을 설정하세요}"

CERT_DIR="$(cd "$(dirname "$0")/.." && pwd)/certs"
CERTBOT_DIR="/tmp/letsencrypt-phantom"

# auth hook: Duck DNS TXT 레코드 설정
AUTH_HOOK=$(cat << 'HOOK'
#!/bin/bash
curl -s "https://www.duckdns.org/update?domains=DOMAIN_PLACEHOLDER&token=TOKEN_PLACEHOLDER&txt=${CERTBOT_VALIDATION}"
sleep 30  # DNS 전파 대기
HOOK
)
AUTH_HOOK="${AUTH_HOOK//DOMAIN_PLACEHOLDER/$DOMAIN}"
AUTH_HOOK="${AUTH_HOOK//TOKEN_PLACEHOLDER/$DUCKDNS_TOKEN}"

# cleanup hook: TXT 레코드 초기화
CLEANUP_HOOK=$(cat << 'HOOK'
#!/bin/bash
curl -s "https://www.duckdns.org/update?domains=DOMAIN_PLACEHOLDER&token=TOKEN_PLACEHOLDER&txt=&clear=true"
HOOK
)
CLEANUP_HOOK="${CLEANUP_HOOK//DOMAIN_PLACEHOLDER/$DOMAIN}"
CLEANUP_HOOK="${CLEANUP_HOOK//TOKEN_PLACEHOLDER/$DUCKDNS_TOKEN}"

# hook 스크립트 생성
AUTH_FILE=$(mktemp)
CLEANUP_FILE=$(mktemp)
echo "$AUTH_HOOK" > "$AUTH_FILE"
echo "$CLEANUP_HOOK" > "$CLEANUP_FILE"
chmod +x "$AUTH_FILE" "$CLEANUP_FILE"
trap "rm -f $AUTH_FILE $CLEANUP_FILE" EXIT

echo "=== Let's Encrypt 인증서 발급 (DNS-01) ==="
echo "도메인: $FQDN"

certbot certonly --manual \
  --preferred-challenges dns \
  --manual-auth-hook "$AUTH_FILE" \
  --manual-cleanup-hook "$CLEANUP_FILE" \
  --register-unsafely-without-email --agree-tos --no-eff-email \
  -d "$FQDN" \
  --config-dir "$CERTBOT_DIR/config" \
  --work-dir "$CERTBOT_DIR/work" \
  --logs-dir "$CERTBOT_DIR/logs"

# 인증서 복사
echo "=== 인증서 복사 ==="
mkdir -p "$CERT_DIR/live/$FQDN"
cp "$CERTBOT_DIR/config/live/$FQDN/fullchain.pem" "$CERT_DIR/live/$FQDN/"
cp "$CERTBOT_DIR/config/live/$FQDN/privkey.pem" "$CERT_DIR/live/$FQDN/"

echo ""
echo "=== 완료! ==="
echo "인증서 위치: $CERT_DIR/live/$FQDN/"
echo "서버 업로드: scp -P 22311 -r $CERT_DIR phantom@118.33.122.28:~/phantom/"
