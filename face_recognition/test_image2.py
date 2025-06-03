import cv2
import joblib
import numpy as np
from insightface.app import FaceAnalysis

# Cargar modelo entrenado y encoder
clf = joblib.load("embeddings/classifier.joblib")
le = joblib.load("embeddings/label_encoder.joblib")

# Inicializar modelo de análisis facial
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0)

# Cargar imagen
img_path = "image_test/test_4.jpeg"  # ⚠️ Cambia esto
img = cv2.imread(img_path)

if img is None:
    raise FileNotFoundError(f"No se pudo cargar la imagen: {img_path}")

# Obtener rostros detectados
faces = app.get(img)

THRESHOLD = 0.65  # Umbral para "sin categoría"

for face in faces:
    bbox = face.bbox.astype(int)
    emb = face.embedding

    probs = clf.predict_proba([emb])[0]
    max_prob = np.max(probs)
    pred = np.argmax(probs)

    if max_prob < THRESHOLD:
        name = "sin categoria"
        color = (0, 0, 255)  # rojo
    else:
        name = le.inverse_transform([pred])[0]
        color = (0, 255, 0)  # verde

    # Dibujar resultado
    cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
    label = f"{name} ({max_prob:.2f})"
    cv2.putText(img, label, (bbox[0], bbox[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

# Mostrar imagen
cv2.imshow("Resultado", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

