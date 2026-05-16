from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
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

# Request model
class ChatRequest(BaseModel):
    message: str

# Root route
@app.get("/")
async def root():
    return {
        "message": "NOIR Atelier Backend Running"
    }

# Load business knowledge
def load_knowledge():

    knowledge = ""

    folder = "knowledge"

    if not os.path.exists(folder):
        return "No knowledge folder found."

    for filename in os.listdir(folder):

        if filename.endswith(".txt"):

            path = os.path.join(folder, filename)

            with open(path, "r", encoding="utf-8") as file:
                knowledge += file.read() + "\n\n"

    return knowledge

# Streaming chat route
@app.post("/chat")
async def chat(request: ChatRequest):

    knowledge = load_knowledge()

    prompt = f"""
You are the official AI strategic advisor
of NOIR Atelier.

NOIR Atelier is a luxury Tehran-based
interior architecture and smart-home studio.

Business knowledge:
{knowledge}

Your personality:
- elegant
- minimal
- intelligent
- calm
- premium
- architectural

Communication style:
- refined
- concise
- emotionally intelligent
- strategic
- cinematic

User question:
{request.message}
"""

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