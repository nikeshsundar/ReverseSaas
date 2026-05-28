#!/usr/bin/env sh
set -e

echo "Waiting for database..."
DB_HOST="${DATABASE_URL#*@}"
DB_HOST="${DB_HOST%:*}"
for i in $(seq 1 30); do
  python -c "import socket; s=socket.socket(); s.settimeout(3); s.connect(('${DB_HOST}', 5432)); s.close()" 2>/dev/null && break
  echo "  attempt $i failed, retrying in 2s..."
  sleep 2
done

python -m prisma db push --accept-data-loss

exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
