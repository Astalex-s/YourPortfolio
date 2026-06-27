#!/bin/bash
# Run ONCE on the server to issue the initial SSL certificate.
# After this, auto-renewal is handled by the certbot service in docker-compose.yml.
set -e

DOMAIN="autonode.ru"
EMAIL="astaf.al.mi@gmail.com"
APP_DIR="/root/yourportfolio"

cd "$APP_DIR"

echo ">>> Stopping nginx to free port 80..."
docker compose stop nginx

echo ">>> Issuing certificate via certbot standalone..."
docker run --rm \
  -p 80:80 \
  -v /etc/letsencrypt:/etc/letsencrypt \
  certbot/certbot certonly \
  --standalone \
  --non-interactive \
  --keep-until-expiring \
  -d "$DOMAIN" \
  -d "www.$DOMAIN" \
  --email "$EMAIL" \
  --agree-tos \
  --no-eff-email

echo ">>> Starting all services..."
docker compose up -d

echo ""
echo "Done! Certificate issued for $DOMAIN."
echo "Auto-renewal is active via the certbot container (every 12h check)."
echo "Nginx reloads are scheduled via cron — see the comment in this script."
echo ""
echo "Add this line to root crontab (crontab -e) to reload nginx daily at 03:05:"
echo "  5 3 * * * docker compose -f $APP_DIR/docker-compose.yml exec -T nginx nginx -s reload >> /var/log/nginx-ssl-reload.log 2>&1"
