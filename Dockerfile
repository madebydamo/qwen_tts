FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    sox \
    && rm -rf /var/lib/apt/lists/*

# Create user with uid 1000
RUN groupadd -g 1000 user && useradd -u 1000 -g 1000 -m user

# Install Python packages
RUN pip install --no-cache-dir qwen-tts soundfile torch huggingface_hub[cli]

# Optional: Install flash-attention for better performance (requires CUDA, uncomment if GPU available)
# RUN pip install flash-attn --no-build-isolation

WORKDIR /app

# Default command
CMD ["bash"]