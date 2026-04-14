#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do
    sleep 0.5
done
echo "PostgreSQL is up."

python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear

python manage.py shell << 'PYEOF'
from django.contrib.auth import get_user_model
import os
U = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
if username and password and not U.objects.filter(username=username).exists():
    U.objects.create_superuser(username, "", password)
    print(f"Superuser '{username}' created.")
PYEOF

exec "$@"
