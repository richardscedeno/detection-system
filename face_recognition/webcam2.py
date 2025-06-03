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


        probs = clf.predict_proba([emb])[0]
        max_prob = np.max(probs)
        pred = np.argmax(probs)

        THRESHOLD = 0.65  # puedes probar entre 0.6 y 0.8

        if max_prob < THRESHOLD:
            name = "sin categoria"
            color = (0, 0, 255)  # rojo
        else:
            name = le.inverse_transform([pred])[0]
            color = (0, 255, 0)  # verde


        # Dibujar rectángulo y etiqueta
    cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
    cv2.putText(frame, f"{name} ({max_prob:.2f})", (bbox[0], bbox[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
 

    cv2.imshow("Reconocimiento Facial en Vivo", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

