import chromadb
import requests
import os

# Create Chroma client
client = chromadb.PersistentClient(path="./chroma_db")

# Create collection
collection = client.get_or_create_collection(
    name="noir_knowledge"
)

KNOWLEDGE_FOLDER = "../knowledge"

def get_embedding(text):

    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )

    data = response.json()

    return data["embedding"]

# Read txt files
for filename in os.listdir(KNOWLEDGE_FOLDER):

    if filename.endswith(".txt"):

        path = os.path.join(
            KNOWLEDGE_FOLDER,
            filename
        )

        with open(path, "r", encoding="utf-8") as file:

            content = file.read()

            embedding = get_embedding(content)

            collection.add(
                documents=[content],
                embeddings=[embedding],
                ids=[filename]
            )

            print(f"Added: {filename}")

print("Knowledge base ingestion complete.")