# Job Processing Microservices

This is a containerized, full-stack job processing microservices platform.
It uses Node.js (frontend), FastAPI (API backend), Python (worker jobs), and Redis.

## Prerequisites
- Docker and Docker Compose (v2)
- Git

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone <your-fork-url>
   cd <repository-directory>
   ```

2. **Configure Environment:**
   A `.env.example` is provided. The `docker-compose.yml` defaults handle the configuration natively, but you can copy the file if you wish to override values locally.
   ```bash
   cp .env.example .env
   ```

3. **Start the Application:**
   Bring up the stack using Docker Compose. The services depend on `redis` starting and passing its health checks first before the backend or worker proceed.
   ```bash
   docker compose up -d
   ```

4. **Verify Startup:**
   Check that all exactly four containers are running and marked as `(healthy)`.
   ```bash
   docker compose ps
   ```

5. **Accessing the Application:**
   Navigate in your browser to the web frontend:
   [http://localhost:3000](http://localhost:3000)
   Click "Submit New Job" to test the pipeline.

## System Architecture Highlights
- **Healthchecks**: Deeply integrated healthchecks verify real API liveliness using application requests internally.
- **Resource Constraints**: Capped CPU and Memory usages preventing service leaks from starving others.
- **Zero-Downtime Deployments**: Bundled custom deploy python script locally rolls updates over seamlessly ensuring new instances are healthy prior to routing.
