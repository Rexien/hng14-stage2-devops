FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
RUN useradd -m -r appuser && chown -R appuser /app
COPY --from=builder /root/.local /home/appuser/.local
COPY . .
RUN chown -R appuser /app
ENV PYTHONUNBUFFERED=1
USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import redis, os, sys; r=redis.Redis(host=os.environ.get('REDIS_HOST', 'localhost'), port=int(os.environ.get('REDIS_PORT', 6379)), password=os.environ.get('REDIS_PASSWORD')); r.ping() or sys.exit(1)"
CMD ["python", "worker.py"]
