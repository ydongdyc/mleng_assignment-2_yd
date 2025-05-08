# score_headlines_api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from joblib import load
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO)

# Initialize FastAPI
app = FastAPI()

# Load the embedding model once at startup
embedding_model_path = "/opt/huggingface_models/all-MiniLM-L6-v2"
svm_model_path = "svm_model.joblib"

if os.path.exists(embedding_model_path):
    embedding_model = SentenceTransformer(embedding_model_path)
else:
    logging.warning("Local model not found. Downloading from HuggingFace...")
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load the sentiment classifier model
classifier = load(svm_model_path)

# Define the expected input format for POST requests
class HeadlinesRequest(BaseModel):
    headlines: list


@app.get("/status")
def status():
    logging.info("Status endpoint called.")
    return {"status": "OK"}

@app.post("/score_headlines")
def score_headlines(request: HeadlinesRequest):
    try:
        logging.info(f"Scoring {len(request.headlines)} headlines.")
        embeddings = embedding_model.encode(request.headlines)
        labels = classifier.predict(embeddings)
        return {"labels": labels.tolist()}
    except Exception as e:
        logging.error(f"Error during scoring: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
