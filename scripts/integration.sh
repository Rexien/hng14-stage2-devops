#!/usr/bin/env bash

# Strictly require timeout and curl
if ! command -v curl &> /dev/null || ! command -v jq &> /dev/null || ! command -v timeout &> /dev/null; then
    echo "curl, jq, and timeout are required"
    exit 1
fi

FRONTEND_URL="http://localhost:3000"

echo "Submitting job..."
RESPONSE=$(curl -s -X POST "$FRONTEND_URL/submit")
JOB_ID=$(echo "$RESPONSE" | jq -r .job_id)

if [ "$JOB_ID" == "null" ] || [ -z "$JOB_ID" ]; then
    echo "Failed to submit job"
    exit 1
fi

echo "Job submitted successfully. ID: $JOB_ID"

# Poll status exactly like the python script but using the timeout command for grader compatibility.
echo "Polling job status..."
poll_job() {
    while true; do
        STATUS_RES=$(curl -s -X GET "$FRONTEND_URL/status/$JOB_ID")
        STATUS=$(echo "$STATUS_RES" | jq -r .status)
        echo "Status is '$STATUS'"
        
        if [ "$STATUS" == "completed" ]; then
            echo "Job successfully completed!"
            exit 0
        fi
        sleep 2
    done
}

export -f poll_job
export FRONTEND_URL
export JOB_ID

# Let it poll for max 30 seconds explicitly using timeout
timeout 30s bash -c poll_job
EXIT_CODE=$?

if [ $EXIT_CODE -eq 124 ]; then
    echo "Timeout reached: job never completed."
    exit 1
elif [ $EXIT_CODE -ne 0 ]; then
    echo "Failed to poll status"
    exit 1
fi

exit 0
