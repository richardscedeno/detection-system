import cv2
import joblib
import numpy as np
from insightface.app import FaceAnalysis

# Cargar modelos
clf = joblib.load("embeddings/classifier.joblib")
le = joblib.load("embeddings/label_encoder.joblib")

# Preparar modelo ArcFace
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0)

# Iniciar cámara
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    raise RuntimeError("❌ No se pudo abrir la cámara")

print("🎥 Cámara iniciada. Presiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    faces = app.get(frame)

    for face in faces:
        bbox = face.bbox.astype(int)
        emb = face.embedding
        pred = clf.predict([emb])[0]
        prob = clf.predict_proba([emb])[0].max()
        name = le.inverse_transform([pred])[0]

        # Dibujar rectángulo y etiqueta
        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
        label = f"{name} ({prob:.2f})"
        cv2.putText(frame, label, (bbox[0], bbox[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("Reconocimiento Facial en Vivo", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

