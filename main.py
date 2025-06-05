from fastapi import APIRouter, HTTPException, Response,FastAPI,File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import whisper
import os
import datetime as time
from celery_worker import transcribe_audio
from celery.result import AsyncResult
from celery_worker import app as celery_app
import tempfile

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.environ["PYTORCH_CUDA_ALLOC_CONF"]="expandable_segments:True"


@app.post("/api/v1/whisper")
async def transcript(file : UploadFile):

    # file=file.file
    
    # print(type(file))
    # stt = whisper.load_model("turbo").to("cuda")
    cwd=os.getcwd()
    path=os.path.join(cwd, "temp.wav")
    if os.path.exists(path):
       os.remove(path)
    with open(path, "wb") as f:
        f.write(await file.read())
        task = transcribe_audio.delay(path)

        
    return {"task_id": task.id}
    
    # start_time=time.datetime.now()
    # result=stt.transcribe(path,language="fa")
    # transcribe_audio.delay(path
    # if os.path.exists(path):
    #     os.remove(path)
        
    
    # text = result["text"].strip()
    # end_time=time.datetime.now()
    # total_time= end_time - start_time
    # print(f"Transcription completed in {end_time - start_time} seconds")
    # return text
    # with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
    #     contents = await file.read()
    #     tmp.write(contents)
    #     tmp.flush()
    #     task = transcribe_audio.delay(tmp.name)
    #     return {"task_id": task.id}

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    print(f"Checking result for task_id: {task_id}, status: {result.status}")
    if result.ready():
        return result.result["text"]
    return {"status": "processing"}

