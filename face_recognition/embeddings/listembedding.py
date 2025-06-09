import numpy as np

embeddings = np.load('embeddings.npy')
labels = np.load('labels.npy')

for i, label in enumerate(labels):
    print(f"Index {i} -> Nombre: {label}")

