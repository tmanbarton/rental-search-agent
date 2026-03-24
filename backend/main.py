import asyncio

import json
from pydantic import BaseModel
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from agent import run_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

messages = []

class SearchRequest(BaseModel):
    user_input: str

def format_sse(event: str, data: dict) -> str:
    """Format a server event string for SSE."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"

@app.post("/search")
async def search(request: SearchRequest):
    async def event_stream():
        async for text in run_agent(request.user_input, messages):
            yield format_sse("status", {"message": text})

    return StreamingResponse(event_stream(), media_type="text/event-stream")

if __name__ == "__main__":
     import uvicorn
     uvicorn.run("main:app", reload=True)


