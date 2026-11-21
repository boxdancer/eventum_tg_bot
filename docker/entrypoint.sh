#!/bin/sh
set -eu

.venv/bin/alembic upgrade head
exec "$@"
