#!/usr/bin/env bash
# Render build script — runs during deploy
set -euo pipefail

echo "=== Installing Python dependencies ==="
pip install -r backend/requirements.txt

echo "=== Installing frontend dependencies ==="
cd frontend
npm install

echo "=== Building frontend ==="
npm run build

echo "=== Build complete ==="
