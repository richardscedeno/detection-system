import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import joblib

# Cargar embeddings
embeddings = np.load("embeddings/embeddings.npy")
labels = np.load("embeddings/labels.npy")

# Codificar etiquetas
le = LabelEncoder()
y = le.fit_transform(labels)

# Entrenar clasificador
clf = SVC(kernel='linear', probability=True)
clf.fit(embeddings, y)

# Guardar modelos
joblib.dump(clf, "embeddings/classifier.joblib")
joblib.dump(le, "embeddings/label_encoder.joblib")
print("✅ Clasificador entrenado y guardado.")

