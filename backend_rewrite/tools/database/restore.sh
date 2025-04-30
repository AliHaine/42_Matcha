#!/bin/bash
set -e
echo "Restoring dump into database..."
createdb "$POSTGRES_USER" -U "$POSTGRES_USER"
pg_restore --no-owner -U "$POSTGRES_USER" -d "$POSTGRES_DB" /docker-entrypoint-initdb.d/sauvegarde.dump