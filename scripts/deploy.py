import subprocess
import time
import sys
import json

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def get_health(container_id):
    stdout, _, _ = run_cmd(f"docker inspect --format='{{{{json .State.Health.Status}}}}' {container_id}")
    return stdout.strip('"')

def rolling_update(service):
    print(f"--- Rolling update for {service} ---")
    
    # 1. Identify the current running container for the service
    # The container name format depends on compose. Usually `repo_folder-service-1`.
    # Let's search by compose project and service labels.
    project_label_filter = ""  # We can just filter by service label
    stdout, _, _ = run_cmd(f"docker ps -q --filter label=com.docker.compose.service={service}")
    old_cids = stdout.split()
    old_cid = old_cids[0] if old_cids else None

    # 2. To avoid downtime and ensure health, we scale the service to 2.
    # docker-compose automatically names it with suffix -2.
    # We must build the new image first.
    print("Building new image...")
    run_cmd(f"docker compose build {service}")

    print("Starting new container instance...")
    # Scale to 2, don't recreate the existing one.
    run_cmd(f"docker compose up -d --no-deps --scale {service}=2 --no-recreate {service}")

    # 3. Find the newly created container
    stdout, _, _ = run_cmd(f"docker ps -q --filter label=com.docker.compose.service={service}")
    current_cids = stdout.split()
    
    new_cid = None
    for cid in current_cids:
        if cid != old_cid:
            new_cid = cid
            break

    if not new_cid:
        print("Failed to identify the new container!")
        # Revert scale
        run_cmd(f"docker compose up -d --no-deps --scale {service}=1 {service}")
        sys.exit(1)

    # 4. Wait for the new container to become healthy
    print(f"Waiting up to 60 seconds for new container {new_cid} to become healthy...")
    healthy = False
    for i in range(30):
        status = get_health(new_cid)
        if status == "healthy":
            healthy = True
            break
        time.sleep(2)

    # 5. Take action based on health
    if healthy:
        print("New container is healthy! Stopping the old container...")
        if old_cid:
            run_cmd(f"docker stop {old_cid}")
            run_cmd(f"docker rm {old_cid}")
        print("Update successful!")
    else:
        print("New container failed to become healthy within 60 seconds. Aborting and rolling back...")
        run_cmd(f"docker stop {new_cid}")
        run_cmd(f"docker rm {new_cid}")
        sys.exit(1)

if __name__ == "__main__":
    for s in ["api", "worker", "frontend"]:
        rolling_update(s)
