#!/bin/bash
# Run on the server to configure the nginx reload cron for certificate renewal.
# The certbot container renews the cert; cron reloads nginx to apply it.
set -e

APP_DIR="/root/yourportfolio"
CRON_LINE="5 3 * * * docker compose -f $APP_DIR/docker-compose.yml exec -T nginx nginx -s reload >> /var/log/nginx-ssl-reload.log 2>&1"

(crontab -l 2>/dev/null | grep -qF "nginx-ssl-reload") && {
  echo "Cron job already exists, skipping."
  exit 0
}

(crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -
echo "Cron job added: nginx reloads daily at 03:05 to pick up renewed certificates."
