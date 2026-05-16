import chromadb
import requests

# Load persistent database
client = chromadb.PersistentClient(
    path="./rag/chroma_db"
)

collection = client.get_collection(
    name="noir_knowledge"
)

# Generate embedding
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

# Retrieve relevant documents
def retrieve_context(query):

    embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=3
    )

    documents = results["documents"][0]

    context = "\n\n".join(documents)

    return context