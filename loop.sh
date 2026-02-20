#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-build}"
MAX="${2:-0}"
COUNT=0
LOG="logs/$(date +%Y%m%d_%H%M%S).log"
mkdir -p logs

echo "=== Ralph Buyback Research Loop ==="
echo "Mode: $MODE | Max iterations: ${MAX:-unlimited}"
echo "Log: $LOG"
echo "Started: $(date)"

while :; do
  echo "--- Iteration $((COUNT + 1)) | $(date) ---" | tee -a "$LOG"

  if [[ "$MODE" == "plan" ]]; then
    cat PROMPT_plan.md | claude -p \
      --dangerously-skip-permissions \
      --model opus \
      --output-format stream-json 2>&1 | tee -a "$LOG"
  else
    cat PROMPT_build.md | claude -p \
      --dangerously-skip-permissions \
      --model opus \
      --output-format stream-json 2>&1 | tee -a "$LOG"
  fi

  COUNT=$((COUNT + 1))
  echo "Completed iteration $COUNT at $(date)" | tee -a "$LOG"

  [[ "$MAX" -gt 0 && "$COUNT" -ge "$MAX" ]] && break

  # Brief pause between iterations
  sleep 5
done

echo "=== Loop complete: $COUNT iterations ==="
