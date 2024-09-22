from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import sys
import os
src_path = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.append(src_path)
from src.query_data import query_rag, QueryResponse
from src.query_model import QueryModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your Flutter web app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SubmitQueryRequest(BaseModel):
    query_text: str


@app.get("/")
def index():
    return {"Hello": "World"}

@app.get("/get_input")


@app.post("/submit_input")
def submit_input_endpoint(request: SubmitQueryRequest) -> QueryResponse:
    response = query_rag(request.query_text)
    return response

if __name__ == "__main__":
    # Run this as a server directly.
    port = 8000
    print(f"Running the FastAPI server on port {port}.")
    uvicorn.run("api_handler:app", host="127.0.0.1", port=port)
