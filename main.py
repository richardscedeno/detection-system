import cv2
import joblib
import numpy as np
from insightface.app import FaceAnalysis
from torch import FunctionSchema
from ultralytics import YOLO
import imutils
import functions

# === Cargar modelo de reconocimiento facial ===
clf = joblib.load("face_recognition/embeddings/classifier.joblib")
le = joblib.load("face_recognition/embeddings/label_encoder.joblib")
face_app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
face_app.prepare(ctx_id=0)
THRESHOLD = 0.65

# === Cargar modelo YOLOv8 para armas ===
yolo_model = YOLO('weights/best50.pt')

# === Captura desde webcam === 
cap = cv2.VideoCapture(1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Copia para detección de armas
    yolo_frame = frame.copy()
    yolo_frame = imutils.resize(yolo_frame, width=500)
    results = yolo_model(yolo_frame, conf=0.5, save_crop=True)

    conf = results[0].boxes.conf
    plot_frame = results[0].plot()

    # Acción si se detecta arma
    if conf.nelement() != 0:
        print(f'[ARMAS] Detectado objeto con confianza: {conf.tolist()}')
        functions.notify_last_detection()
    else:
        print('[ARMAS] No se detecta arma.')

    # === Detección y reconocimiento facial ===
    faces = face_app.get(frame)

    for face in faces:
        bbox = face.bbox.astype(int)
        emb = face.embedding

        probs = clf.predict_proba([emb])[0]
        max_prob = np.max(probs)
        pred = np.argmax(probs)

        if max_prob < THRESHOLD:
            name = "sin categoría"
            color = (0, 0, 255)  # rojo
        else:
            name = le.inverse_transform([pred])[0]
            color = (0, 255, 0)  # verde

        label = f"{name} ({max_prob:.2f})"
        cv2.rectangle(plot_frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
        cv2.putText(plot_frame, label, (bbox[0], bbox[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Mostrar todo en la misma ventana
    cv2.imshow("Armas + Rostros", plot_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

