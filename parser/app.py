from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from parser import python_parse_file, python_parse_folder, dump_ast

app = FastAPI()
class CodeRequest(BaseModel):
    code: str

class FileRequest(BaseModel):
    file_path: str

@app.post("/toLower")
def to_lower(request: CodeRequest):
    """Test route to check if the FastAPI app is working"""
    return {"result": request.code.lower()}

@app.get("/healthy")
def healthy():
    """Route that provides an endpoint for the Docker health check."""
    return "yay"

@app.post("/py/file")
def py_file(request: FileRequest):
    try:
        ast_tree = python_parse_file(request.file_path)
        # Serialize the AST tree to a string for JSON response
        ast_json = dump_ast(ast_tree)
        return {"ast": ast_json}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))