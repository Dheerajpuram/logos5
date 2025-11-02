import os
import shutil
from typing import List, Dict, Any, Union
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from router import route_query
from csv_handler import answer_from_csv
from rag_handler import answer_from_rag
from sql_handler import answer_from_sql

load_dotenv()

app = FastAPI(
    title="Multi-Source AI Copilot",
    description="A conversational business intelligence agent that can query and analyze data from multiple sources.",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# --- Pydantic Models ---
class Query(BaseModel):
    query: str
    selected_files: List[str] = []

class UploadResponse(BaseModel):
    filename: str
    path: str

class AskResponse(BaseModel):
    source: str
    answer: Union[str, List[Dict[str, Any]], None] = None
    query: str | None = None

# --- API Endpoints ---
@app.get("/", tags=["General"], summary="Root endpoint")
def read_root():
    """Returns a simple hello world message."""
    return {"Hello": "World"}

@app.get("/api/files", tags=["Data"], summary="List files in the data directory")
def list_files():
    """Lists all files in the data directory."""
    data_dir = "/Users/dheeraj/Desktop/finalmp/data"
    files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
    return {"files": files}

@app.get("/api/key", tags=["Debugging"], summary="Get Gemini API Key")
def get_key():
    """Returns the configured Gemini API key (for debugging purposes)."""
    return {"api_key": os.getenv("GEMINI_API_KEY")}

@app.post("/api/upload", response_model=UploadResponse, tags=["Data"], summary="Upload a file")
async def upload_file(file: UploadFile = File(...)):
    """Uploads a file (PDF or CSV) to the data directory."""
    file_path = os.path.join("/Users/dheeraj/Desktop/finalmp/data", file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "path": file_path}

@app.post("/api/ask", response_model=AskResponse, tags=["AI"], summary="Ask a question")
def ask(query: Query):
    """Routes a natural language query to the appropriate data source and returns an answer."""
    print(f"--- Received query: {query.query} ---")
    source = route_query(query.query)
    print(f"--- Routed to: {source} ---")

    if source == "CSV":
        answer = answer_from_csv(query.query)
        return {"source": source, "answer": answer}
    elif source == "RAG":
        answer = answer_from_rag(query.query, query.selected_files)
        return {"source": source, "answer": answer}
    elif source == "SQL":
        answer = answer_from_sql(query.query)
        return {"source": source, "answer": answer}
    else:
        return {"source": "Unknown", "query": query.query}