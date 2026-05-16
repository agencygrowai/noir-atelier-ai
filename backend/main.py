from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag.retrieval import retrieve_context

import requests
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Message model
class Message(BaseModel):
    role: str
    content: str

# Request model
class ChatRequest(BaseModel):
    message: str
    history: list[Message]

# Root route
@app.get("/")
async def root():

    return {
        "message": "NOIR Atelier AI Backend Running"
    }

# Streaming chat route
@app.post("/chat")
async def chat(request: ChatRequest):

    # Retrieve semantic RAG context
    knowledge = retrieve_context(
        request.message
    )

    # Build conversation memory
    conversation_history = ""

    for msg in request.history:

        role = msg.role.upper()

        conversation_history += (
            f"{role}: {msg.content}\n"
        )

    # Final AI prompt
    prompt = f"""
You are the official AI strategic advisor
of NOIR Atelier.

NOIR Atelier is a luxury Tehran-based
interior architecture and smart-home studio.

You are speaking to:
- luxury apartment owners
- investors
- architects
- startup founders
- premium clients

Relevant business knowledge:
{knowledge}

Conversation history:
{conversation_history}

Your personality:
- elegant
- minimal
- intelligent
- strategic
- emotionally refined
- calm
- architectural

Communication style:
- cinematic
- premium
- concise
- insightful
- sophisticated

Behavior rules:
- Never sound generic
- Maintain conversational continuity
- Remember previous discussion context
- Speak like a premium strategist
- Prioritize emotional intelligence
- Use retrieved knowledge naturally
- Keep answers refined and thoughtful

Current user message:
{request.message}
"""

    # Streaming generator
    def generate():

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.1:8b",
                "prompt": prompt,
                "stream": True
            },
            stream=True
        )

        for line in response.iter_lines():

            if line:

                try:

                    json_data = json.loads(line)

                    if "response" in json_data:
                        yield json_data["response"]

                except:
                    pass

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )