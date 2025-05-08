# Headline Sentiment Scoring API

This project serves a trained headline sentiment analysis model as a web service using FastAPI.

Clients can make real-time requests to classify the sentiment of news headlines into one of three labels:
- **Optimistic**
- **Pessimistic**
- **Neutral**

---

## 🚀 How to Run the API Locally

1. Install dependencies:

```bash
pip install fastapi uvicorn sentence-transformers scikit-learn joblib
```

2. Start the FastAPI server:

```bash
uvicorn score_headlines_api:app --host 0.0.0.0 --port 8084
```

(You can replace 8084 with another port locally if needed.)

3. Access the interactive API docs (Swagger UI) at:

> [http://127.0.0.1:8084/docs](http://127.0.0.1:8084/docs)

---

## 📬 API Endpoints

### 1. `/status` (GET)
- Returns `{"status": "OK"}` to confirm that the server is live.

Example:

```bash
curl http://127.0.0.1:8084/status
```

---

### 2. `/score_headlines` (POST)
- Accepts a **JSON object** with a list of headlines.
- Returns a list of sentiment labels corresponding to each headline.

### Request Format (JSON)

```json
{
  "headlines": [
    "First headline here",
    "Second headline here",
    "Third headline here"
  ]
}
```

### Example Curl Command

```bash
curl -X POST "http://127.0.0.1:8084/score_headlines" -H "Content-Type: application/json" -d "{\"headlines\":[\"Stock market rallies\",\"Economic fears mount\"]}"
```

### Example Response

```json
{
  "labels": ["Optimistic", "Pessimistic"]
}
```

---

## ⚙️ Model Loading Details

- The **sentence transformer** model (`all-MiniLM-L6-v2`) is loaded once at server startup.
- The **sentiment SVM classifier** (`svm_model.joblib`) is also loaded once.
- This ensures **fast, real-time scoring** without reloading models per request.

If `/opt/huggingface_models/all-MiniLM-L6-v2` is not found, the server automatically downloads the model from HuggingFace on first run.

---

## 🛠 Development Notes

- Logging is handled using Python’s `logging` library.
- Logs important events such as:
  - API endpoint calls (`info`)
  - Errors during scoring (`error`)
- Server should be stopped (`Ctrl+C`) when not actively testing to minimize security exposure.

---

## 🌍 Deployment on Virtual Machine

1. SSH into the VM.
2. `git pull` the latest code.
3. Run:

```bash
uvicorn score_headlines_api:app --host 0.0.0.0 --port 8084
```

(Use assigned port: 8084)

4. Test from local machine with:

```bash
curl http://your_vm_ip:8084/status
```

or visit in browser:

> http://your_vm_ip:8084/docs

---

# ✅ Summary

This API is ready for real-time headline sentiment classification, supports both programmatic and browser-based usage, and is designed for minimal server load and bandwidth optimization.
