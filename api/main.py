import sys

sys.path.append("..") 

import epicgames_claimer
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/epicgames-claimer/v1/latest_version")
def latest_version():
    return epicgames_claimer.__version__

@app.get("/epicgames-claimer/v1/epicgames_claimer.py")
def epicgames_claimer_py():
    return FileResponse("../epicgames_claimer.py")
