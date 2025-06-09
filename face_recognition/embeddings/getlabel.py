import joblib

# Cargar el LabelEncoder
label_encoder = joblib.load('label_encoder.joblib')

# Mostrar la relación indice <-> nombre
print('Índice | Nombre')
print('----------------')
for idx, nombre in enumerate(label_encoder.classes_):
    print(f'{idx:<6} | {nombre}')
