#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FastAPI backend for MetaGPT Chat Interface
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, HTMLResponse
from pydantic import BaseModel
import asyncio
from pathlib import Path
import sys
import os

# Add parent directory to path to import metagpt
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set default config path if in Docker
if os.path.exists('/app/config/config2.yaml'):
    os.environ.setdefault('CONFIG_ROOT', '/app/config')
    
    # Override service_account_path to use container path
    import yaml
    config_path = '/app/config/config2.yaml'
    try:
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        
        # Update service_account_path to container path if it's a host path
        if 'llm' in config_data and 'service_account_path' in config_data['llm']:
            old_path = config_data['llm']['service_account_path']
            # If path contains host path, replace with container path
            if '/home/' in old_path or old_path.startswith('/'):
                config_data['llm']['service_account_path'] = '/app/config/service-account.json'
                
                # Write updated config
                with open(config_path, 'w') as f:
                    yaml.dump(config_data, f, default_flow_style=False)
    except Exception as e:
        print(f"Warning: Could not update config: {e}")

from metagpt.llm import LLM
from metagpt.logs import log_llm_stream, create_llm_stream_queue, get_llm_stream_queue

app = FastAPI(title="MetaGPT Chat API")

# Get the directory where main.py is located
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

class ChatRequest(BaseModel):
    message: str
    stream: bool = True

class ChatResponse(BaseModel):
    response: str

# Initialize LLM lazily
llm = None

def get_llm():
    global llm
    if llm is None:
        llm = LLM()
    return llm

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    html_path = STATIC_DIR / "index.html"
    with open(html_path, "r") as f:
        return f.read()

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Stream chat responses"""
    async def generate():
        try:
            llm_instance = get_llm()
            # Create a queue for streaming
            queue = create_llm_stream_queue()
            
            # Start the LLM request in a separate task
            async def get_response():
                response = await llm_instance.aask(request.message)
                # Send end marker
                await queue.put(None)
                return response
            
            # Start the task
            task = asyncio.create_task(get_response())
            
            # Stream the response
            while True:
                try:
                    chunk = await asyncio.wait_for(queue.get(), timeout=0.1)
                    if chunk is None:  # End marker
                        break
                    yield f"data: {chunk}\n\n"
                except asyncio.TimeoutError:
                    # Check if task is done
                    if task.done():
                        break
                    continue
            
            # Ensure task is complete
            await task
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"
            yield "data: [DONE]\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Non-streaming chat endpoint"""
    try:
        llm_instance = get_llm()
        response = await llm_instance.aask(request.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
