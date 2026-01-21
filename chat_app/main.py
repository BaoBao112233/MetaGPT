#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FastAPI backend for MetaGPT Chat Interface
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, HTMLResponse, FileResponse
from pydantic import BaseModel

# Add parent directory to path to import metagpt
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from metagpt.const import DEFAULT_WORKSPACE_ROOT
from chat_app.manager import MetaGPTManager

app = FastAPI(title="MetaGPT Chat API")

# Workspaces and static directories
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
WASHROOM_DIR = ROOT_DIR / "workspace"

manager = MetaGPTManager(workspace_path=WASHROOM_DIR)

# Ensure static directory exists
STATIC_DIR.mkdir(exist_ok=True)

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Stream chat response including reasoning/logs
    """
    async def event_generator():
        async for item in manager.run_project(request.message):
            yield f"data: {json.dumps(item)}\n\n"
        yield "data: {\"type\": \"done\"}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/api/files")
async def list_files():
    """
    List all generated files in the workspace
    """
    return manager.get_generated_files()

@app.get("/api/files/{file_path:path}")
async def get_file(file_path: str):
    """
    Download a specific file from the workspace
    """
    full_path = WASHROOM_DIR / file_path
    if not full_path.exists() or not full_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(full_path, filename=full_path.name)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Serve the frontend (will be built and placed in static/ or handled by Vite dev server)
# For now, if index.html exists in static, serve it. 
# Otherwise, we might be in development mode using Vite.
@app.get("/{rest_of_path:path}")
async def serve_frontend(rest_of_path: str):
    if rest_of_path.startswith("api/") or rest_of_path == "health":
        raise HTTPException(status_code=404)
        
    file_path = STATIC_DIR / rest_of_path
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    
    # Fallback to index.html for SPA
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
        
    return HTMLResponse("Frontend not found. Please build the frontend first.", status_code=404)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
