from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
class CodeRequest(BaseModel):
    code: str

@app.post("/toLower")
def to_lower(request: CodeRequest):
    """Test route to check if the FastAPI app is working"""
    return {"result": request.code.lower()}

@app.get("/healthy")
def healthy():
    """Route that provides an endpoint for the Docker health check."""
    return "yay"

@app.post("/py/file")
def py_file():
    return "nothing"
