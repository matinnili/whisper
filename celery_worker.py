from celery import Celery
import whisper

app = Celery("worker", broker="redis://redis:6379/0")
model = whisper.load_model("base")

@app.task
def transcribe_audio(filepath):
    result = model.transcribe(filepath)
    return result