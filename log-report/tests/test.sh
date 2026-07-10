#!/usr/bin/env bash
set -uo pipefail

LOGS_DIR="/logs/verifier"
mkdir -p "$LOGS_DIR"

# Run pytest with CTRF JSON output — deps already in the image, no installs needed
pytest /tests/test_outputs.py \
    --json-ctrf "$LOGS_DIR/ctrf.json" \
    -v > "$LOGS_DIR/pytest.log" 2>&1 \
  && echo "1" > "$LOGS_DIR/reward.txt" \
  || echo "0" > "$LOGS_DIR/reward.txt"

exit 0
