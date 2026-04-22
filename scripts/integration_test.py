import requests
import time
import sys

FRONTEND_URL = "http://localhost:3000"

def test_integration():
    print("Submitting job...")
    try:
        response = requests.post(f"{FRONTEND_URL}/submit")
        response.raise_for_status()
        data = response.json()
        job_id = data.get("job_id")
        print(f"Job submitted successfully. ID: {job_id}")
    except Exception as e:
        print(f"Failed to submit job: {e}")
        sys.exit(1)

    print("Polling job status...")
    max_retries = 15
    for i in range(max_retries):
        try:
            status_res = requests.get(f"{FRONTEND_URL}/status/{job_id}")
            status_res.raise_for_status()
            status_data = status_res.json()
            status = status_data.get("status")
            print(f"Attempt {i+1}: Status is '{status}'")
            if status == "completed":
                print("Job successfully completed!")
                sys.exit(0)
            time.sleep(2)
        except Exception as e:
            print(f"Failed to poll status: {e}")
            sys.exit(1)

    print("Timeout reached: job never completed.")
    sys.exit(1)

if __name__ == "__main__":
    test_integration()
