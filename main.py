from fastapi import APIRouter, HTTPException, Response,FastAPI,File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import whisper
import os
import datetime as time

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.environ["PYTORCH_CUDA_ALLOC_CONF"]="expandable_segments:True"


@app.get("/api/v1/whisper")
async def transcript():

    # file=file.file
    
    # print(type(file))
    
    cwd=os.getcwd()
    path=os.path.join(cwd, "temp.wav")
    # with open(path, "wb") as f:
    #     f.write(await file.read())
    
    start_time=time.datetime.now()
    result=await transcribe(path)
    
    # if os.path.exists(path):
    #     os.remove(path)
        
    
    text = result["text"].strip()
    end_time=time.datetime.now()
    total_time= end_time - start_time
    print(f"Transcription completed in {end_time - start_time} seconds")
    return text

async def transcribe(path):
    stt = whisper.load_model("large").to("cuda")
    result=stt.transcribe(path,language="fa")
    return result
