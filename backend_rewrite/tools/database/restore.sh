#!/bin/bash
set -e
echo "Restoring dump into database..."
pg_restore --no-owner -U "$POSTGRES_USER" -d "$POSTGRES_DB" /docker-entrypoint-initdb.d/sauvegarde.dump