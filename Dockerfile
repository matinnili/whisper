FROM python:3.10

# Set environment variables for pip
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libsndfile1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pip packages with extended timeout and retries
WORKDIR /app
COPY ./requirements.txt /app/
RUN pip3 install --upgrade pip && \
    pip3 install torch --extra-index-url https://download.pytorch.org/whl/cpu && \
    pip3 install git+https://github.com/openai/whisper.git \
    pip3 install fastapi


COPY . /app/

CMD  ["fastapi", "run", "main.py", "--port", "80","--reload"]