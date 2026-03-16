FROM python:3.12-slim

ARG UID=1000
ARG GID=1000

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    sox \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -g ${GID} appuser || true && useradd -u ${UID} -g ${GID} -m -s /bin/bash appuser || true

RUN mkdir -p /app/models && chown -R appuser:appuser /app

RUN pip install --no-cache-dir qwen-tts soundfile torch huggingface_hub[cli]

WORKDIR /app

USER appuser

CMD ["bash"]
