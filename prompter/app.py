from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from prompter import build_docu

app = FastAPI()

class ASTRequest(BaseModel):
    ast: str

@app.get("/healthy")
def healthy():
    """Route that provides an endpoint for the Docker health check."""
    return "yay"

@app.post("/docu")
def docu(request: ASTRequest):
    try:    
        result = build_docu(request.ast)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))