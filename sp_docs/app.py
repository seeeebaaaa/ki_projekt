from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from gen_docu import sphinx_gen_docs

app = FastAPI()

class FileRequest(BaseModel):
    path: str

@app.get("/healthy")
def healthy():
    """Route that provides an endpoint for the Docker health check."""
    return "yay"

@app.post("/docs")
def docu(request: FileRequest):
    try:    
        result = sphinx_gen_docs(request.path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))