# Fixes

| File | Line | Bug Description | Fix Applied |
| :--- | :--- | :--- | :--- |
| `api/main.py` | 8 | Hardcoded `redis.Redis(host="localhost", ...)` lacks credentials and uses a fixed local host preventing container connection. | Replaced with `os.environ.get()` to pull `REDIS_HOST`, `REDIS_PORT`, and `REDIS_PASSWORD`. |
| `worker/worker.py` | 6 | Hardcoded `redis.Redis(host="localhost", ...)` preventing distributed connection to Redis service. | Replaced with `os.environ.get()` to dynamically define connection variables. |
| `worker/worker.py` | 14-18 | `process_job` throws errors when redis fails, crashing the whole worker process. | Wrapped the inner while-loop block with a `try-except` block to log errors and gracefully recover. |
| `frontend/app.js` | 6 | `API_URL` hardcoded to `http://localhost:8000` which breaks when frontend runs in a container. | Modified to use `process.env.API_URL || "http://localhost:8000"` allowing dynamic configuration. |
| `api/.env` | 1 | Included hardcoded secrets `REDIS_PASSWORD=supersecretpassword123` tracked in `.git` history. | Removed file from the repository and scrubbed it from the git history completely. |
| `api/main.py` | 17-18 | Critical race condition: `lpush` is called before `hset`, allowing the worker to pop and complete the job before the API initializes the `status` to `queued`. | Swapped operations: `hset` is performed before `lpush` to guarantee initial state exists before queuing. |
| `worker/Dockerfile` | 12 | Python natively buffers stdout effectively swallowing print logs (`print(f"Processing... "`) inside Docker networks. | Injected `ENV PYTHONUNBUFFERED=1` inside the Dockerfiles ensuring stdout streams consistently. |
