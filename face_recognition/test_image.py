import cv2
import joblib
import numpy as np
from insightface.app import FaceAnalysis

# Cargar modelos
clf = joblib.load("embeddings/classifier.joblib")
le = joblib.load("embeddings/label_encoder.joblib")

# InsightFace
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0)

# Ruta de prueba
img_path = "image_test/test_4.jpeg"
img = cv2.imread(img_path)

faces = app.get(img)
if faces:
    emb = faces[0].embedding
    pred = clf.predict([emb])[0]
    prob = clf.predict_proba([emb])[0].max()
    name = le.inverse_transform([pred])[0]
    print(f"✅ Predicción: {name} (confianza: {prob:.2f})")
else:
    print("❌ No se detectó rostro.")

