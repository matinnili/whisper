FROM python:3.10-slim

# Set environment variables for pip
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=600 \
    PIP_RETRIES=20

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libsndfile1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pip packages with extended timeout and retries
COPY ./requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install torch --extra-index-url https://download.pytorch.org/whl/cpu && \
    pip install git+https://github.com/openai/whisper.git \
    pip install -r requirements.txt
COPY . /app/

CMD  ["fastapi", "run", "main.py", "--port", "80","--reload"]