from celery import Celery
import whisper

app = Celery("worker", broker="redis://redis:6379/0",backend="redis://redis:6379/0")


@app.task
def transcribe_audio(filepath):
    model = whisper.load_model("base").to("cuda")
    print(f"----------------- hi i'm here")
    result = model.transcribe(filepath)
    
    return result