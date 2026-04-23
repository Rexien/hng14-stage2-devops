FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
RUN groupadd -r appgroup && useradd -r -g appgroup appuser && chown -R appuser:appgroup /app
COPY --from=builder /root/.local /home/appuser/.local
COPY . .
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*
RUN chown -R appuser /app
ENV PYTHONUNBUFFERED=1
USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request, sys; urllib.request.urlopen('http://localhost:8000/docs') or sys.exit(1)"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
