# 🧠 Biometric-IA — Facial Verification API (FastAPI + InsightFace + Docker)

**Biometric-IA** is a local biometric authentication microservice that uses **facial recognition** to verify a person’s identity by comparing a **selfie** with the **photo printed on a Mexican INE ID**.  
Built with **FastAPI** and **InsightFace**, the system generates a **match score (0 to 1)** indicating how similar both faces are, allowing you to confirm if the user is the same person.

---

## 🚀 Main Features
- 📸 **Local facial comparison:** runs fully offline, no external APIs required.  
- 🤖 **`buffalo_l` AI model:** pre-trained InsightFace model for high-accuracy facial recognition.  
- ⚡ **Simple REST API:** `/verify` endpoint accepts images and returns a JSON response.  
- 🔒 **Privacy-first design:** images are processed in memory and never stored.  
- 🐳 **Docker and Docker Compose ready:** easy to deploy and portable.  
- 🔁 **Integrates easily with Node.js** or any backend via HTTP POST.

---

## 🧩 Technologies Used
- [Python 3.11](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [InsightFace](https://github.com/deepinsight/insightface)
- [ONNX Runtime](https://onnxruntime.ai/)
- [OpenCV](https://opencv.org/)
- [NumPy](https://numpy.org/)
- [Docker](https://www.docker.com/)

---

## ⚙️ Project Structure
```
biometric-ia/
├─ app.py               # Main FastAPI app
├─ requirements.txt     # Python dependencies
├─ Dockerfile           # Docker image definition
├─ .dockerignore        # Files excluded from Docker build
└─ __pycache__/         # Compiled Python cache (ignored in Git)
```

---

## 💻 Run Locally (without Docker)

1. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .\.venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the service**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8001 --reload
   ```

4. **Check health endpoint**
   - Open: http://localhost:8001/health  
   - Should return: `{"ok": true}`

---

## 🐳 Run with Docker

### 1. Build the image
```bash
docker build -t biometric-ia .
```

### 2. Run the container
```bash
docker run -d -p 8001:8001 --name biometric-ia biometric-ia
```

### 3. Verify the service
Visit http://localhost:8001/health

---

## 🧪 API Example

### ✅ Using cURL
```bash
curl -X POST "http://localhost:8001/verify"   -F "selfie=@C:\images\selfie.jpg"   -F "ine=@C:\images\ine_front.jpg"
```

### ✅ Example JSON Response
```json
{
  "status": "ok",
  "score": 0.7696,
  "cosine_similarity": 0.5391,
  "model": "insightface-buffalo_l"
}
```

> A `score` close to **1.0** indicates a high facial match.  
> You can define your own acceptance threshold, e.g. `score >= 0.5`.

---

## 🧱 Dockerfile (included)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
```

---

## 🧩 Optional: Docker Compose Setup

If you also have a Node.js API that consumes this Python microservice, you can run both together using **Docker Compose**:

```yaml
version: '3.9'
services:
  ia-service:
    build: ./biometric-ia
    ports:
      - "8001:8001"

  node-api:
    build: ./node-api
    ports:
      - "3001:3001"
    environment:
      - PYTHON_IA_URL=http://ia-service:8001
      - THRESHOLD=0.5
```

Run both services:
```bash
docker compose up --build
```

---

## 💡 Recommended Use
Perfect for **hackathons**, **academic projects**, or **local prototypes** that require facial verification **without relying on cloud APIs**.  
Easily integrates with user registration, login, or password recovery systems.

---

## 📜 License
This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute it as long as proper credit is given.

---

