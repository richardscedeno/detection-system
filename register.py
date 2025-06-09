import joblib
import os
from db.insertions import insertar_persona, insertar_persona1

# Ruta al label encoder
LABEL_ENCODER_PATH = os.path.join('face_recognition', 'embeddings', 'label_encoder.joblib')

# Cargar el label encoder
label_encoder = joblib.load(LABEL_ENCODER_PATH)
labels = label_encoder.classes_

# Mostrar los índices y nombres
print("\n--- Lista de personas del dataset ---")
for idx, label in enumerate(labels):
    print(f"{idx} -> {label}")
print("-------------------------------------\n")

# Preguntar si desea registrar a alguien
respuesta = input("¿Desea registrar una persona? (s/n): ").strip().lower()
if respuesta != 's':
    print("Operación cancelada.")
    exit()

# Solicitar índice a registrar
try:
    index = int(input("Ingrese el índice de la persona a registrar: ").strip())
    label = labels[index]
except (ValueError, IndexError):
    print("Índice inválido.")
    exit()

# Extraer tipo y nombre desde el label
try:
    tipo_raw, nombre_completo = label.split('/')
    tipo = tipo_raw.lower()  # 'Docente' -> 'docente'
    nombres_apellidos = nombre_completo.replace('_', ' ').split()
    if len(nombres_apellidos) < 2:
        print("Nombre inválido en el dataset.")
        exit()
    nombre = nombres_apellidos[0]
    apellido = " ".join(nombres_apellidos[1:])
except Exception as e:
    print(f"Error al procesar el nombre: {e}")
    exit()

# Solicitar identificación
identificacion = input("Ingrese la cédula (identificación): ").strip()

# Solicitar datos adicionales si es estudiante
datos_especificos = {}
if tipo == 'estudiante':
    carrera = input("Ingrese la carrera del estudiante: ").strip()
    semestre = input("Ingrese el semestre (número): ").strip()
    datos_especificos = {
        "carrera": carrera,
        "semestre": int(semestre)
    }

# Insertar en base de datos
success, message = insertar_persona(
    tipo=tipo,
    identificacion=identificacion,
    nombre=nombre,
    apellido=apellido,
    datos_especificos=datos_especificos,
    embedding_index=index
)

print(f"\n{message}")

