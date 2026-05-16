from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

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

    # Check if folder exists
    if not os.path.exists(folder):
        return "No knowledge folder found."

    # Read all txt files
    for filename in os.listdir(folder):

        if filename.endswith(".txt"):

            path = os.path.join(folder, filename)

            with open(path, "r", encoding="utf-8") as file:
                knowledge += file.read() + "\n\n"

    return knowledge

# Chat route
@app.post("/chat")
async def chat(request: ChatRequest):

    try:

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
- calm
- intelligent
- premium
- minimal

User question:
{request.message}
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.1:8b",
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()

        return {
            "response": data["response"]
        }

    except Exception as e:

        return {
            "error": str(e)
        }