from fastapi import APIRouter, HTTPException, Response,FastAPI,File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import whisper

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/whisper")
def transcribe(file : UploadFile):

    stt = whisper.load_model("base.en")
    result=stt.transcribe(file, fp16=False)
    text = result["text"].strip()
    return text

