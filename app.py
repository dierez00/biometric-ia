from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import numpy as np
import cv2
from PIL import Image
import io
from typing import Optional
import insightface

app = FastAPI(title="Local IA - Face Match (INE + Selfie)")

# Ajusta det_size si tu CPU sufre: (480,480) o (320,320)
face_app = insightface.app.FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
face_app.prepare(ctx_id=0, det_size=(640, 640))

def read_image_to_bgr(image_bytes: bytes):
    pil = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    arr = np.array(pil)
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

def get_main_face_embedding(bgr) -> Optional[np.ndarray]:
    faces = face_app.get(bgr)
    if not faces:
        return None
    faces.sort(key=lambda f: (f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]), reverse=True)
    return faces[0].normed_embedding  # embedding L2-normalizado

def cosine_to_unit_score(cos_sim: float) -> float:
    return float((cos_sim + 1.0) / 2.0)  # [-1,1] -> [0,1]

@app.post("/verify")
async def verify(selfie: UploadFile = File(...), ine: UploadFile = File(...)):
    try:
        selfie_bytes = await selfie.read()
        ine_bytes = await ine.read()

        emb_self = get_main_face_embedding(read_image_to_bgr(selfie_bytes))
        if emb_self is None:
            raise HTTPException(status_code=422, detail="No se detectó rostro en la selfie.")

        emb_ine = get_main_face_embedding(read_image_to_bgr(ine_bytes))
        if emb_ine is None:
            raise HTTPException(status_code=422, detail="No se detectó rostro en la foto del INE.")

        cos_sim = float(np.dot(emb_self, emb_ine))
        score = cosine_to_unit_score(cos_sim)

        return JSONResponse({
            "status": "ok",
            "score": round(score, 4),
            "cosine_similarity": round(cos_sim, 4),
            "model": "insightface-buffalo_l"
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")

@app.get("/health")
def health():
    return {"ok": True}
