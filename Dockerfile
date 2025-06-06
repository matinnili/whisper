FROM python:3.10-slim

# Set environment variables for pip
WORKDIR /app

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install git -y
# If are experiencing errors ImportError: cannot import name 'soft_unicode' from 'markupsafe'  please uncomment below
# RUN pip3 install markupsafe==2.0.1
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir  openai-whisper
RUN apt-get install -y ffmpeg


COPY . /app/

CMD  ["fastapi", "run", "main.py", "--port", "80","--workers","12"]