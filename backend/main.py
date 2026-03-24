import asyncio

import json
from pydantic import BaseModel
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

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
        yield format_sse("status", {"message": "Starting search..."})
        await asyncio.sleep(1)
        yield format_sse("status", {"message": "Starting listings..."})
        await asyncio.sleep(1)
        yield format_sse("status", {"message": "Fetching HUD data..."})
        await asyncio.sleep(1)
        yield format_sse("status", {"message": "Fetching Census data..."})
        await asyncio.sleep(1)
        yield format_sse("status", {"message": "Done. This is where results will go."})

    return StreamingResponse(event_stream(), media_type="text/event-stream")



