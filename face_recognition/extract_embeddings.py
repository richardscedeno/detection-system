import os
import numpy as np
import cv2
from tqdm import tqdm
from insightface.app import FaceAnalysis

# Configurar el modelo
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0)

# Ruta al dataset
dataset_dir = 'dataset'
embeddings = []
labels = []

# Recorrer las carpetas
for label in os.listdir(dataset_dir):
    label_dir = os.path.join(dataset_dir, label)
    if not os.path.isdir(label_dir):
        continue
    for person in os.listdir(label_dir):
        person_dir = os.path.join(label_dir, person)
        if not os.path.isdir(person_dir):
            continue
        for img_name in tqdm(os.listdir(person_dir), desc=person):
            img_path = os.path.join(person_dir, img_name)
            img = cv2.imread(img_path)
            if img is None:
                continue
            faces = app.get(img)
            if faces:
                emb = faces[0].embedding
                embeddings.append(emb)
                labels.append(f"{label}/{person}")

# Guardar
os.makedirs("embeddings", exist_ok=True)
np.save("embeddings/embeddings.npy", np.array(embeddings))
np.save("embeddings/labels.npy", np.array(labels))
print("✅ Embeddings guardados.")

