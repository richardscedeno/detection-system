from os import wait
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import joblib
import numpy as np
from insightface.app import FaceAnalysis
from ultralytics import YOLO
import functions  # Asegúrate de que notify_last_detection(frame, mensaje=None) lo soporte
from db.queries import obtener_persona_por_indice

# Inicializar modelos
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0)
modelo_armas = YOLO("best50.pt")
clf = joblib.load("face_recognition/embeddings/classifier.joblib")
le = joblib.load("face_recognition/embeddings/label_encoder.joblib")
THRESHOLD = 0.65

# Interfaz
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.geometry("700x550")
root.title("Sistema de detección")

video_label = ctk.CTkLabel(root, width=640, height=360, corner_radius=15, text="")
video_label.pack(pady=20)

cap = None
running = False

# Detección
def detectar_y_mostrar(frame):
    deteccion_realizada = False
    persona_detectada = None

    # Detección de armas
    resultados = modelo_armas(frame, verbose=False)[0]
    for box in resultados.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        label = resultados.names[int(box.cls[0])]
        conf = float(box.conf[0])
        texto = f"{label} ({conf:.2f})"
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, texto, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        deteccion_realizada = True

    # Detección de rostros
    faces = app.get(frame)
    for face in faces:
        bbox = face.bbox.astype(int)
        emb = face.embedding
        probs = clf.predict_proba([emb])[0]
        max_prob = np.max(probs)
        pred = int(np.argmax(probs))

        if max_prob < THRESHOLD:
            name = "Sin categoria"
            color = (0, 0, 255)
        else:
            name = le.inverse_transform([pred])[0]
            persona_detectada = obtener_persona_por_indice(pred)
            color = (0, 255, 0)

        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
        label = f"{name} ({max_prob:.2f})"
        cv2.putText(frame, label, (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Notificación si hay arma
    if deteccion_realizada:
        if persona_detectada:
            mensaje = (
                f"Arma detectada. Persona identificada: "
                f"{persona_detectada['nombre']} {persona_detectada['apellido']} "
                f"({persona_detectada['tipo']})"
            )
        else:
            mensaje = "Arma detectada. Persona no identificada."
        functions.notify_last_detection(frame, mensaje=mensaje)

    return frame

# Loop de video
def actualizar_frame():
    global cap, running
    if running and cap is not None:
        ret, frame = cap.read()
        if ret:
            frame = detectar_y_mostrar(frame)
            frame = cv2.resize(frame, (640, 360))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.configure(image=imgtk)
            video_label.image = imgtk
    if running:
        video_label.after(10, actualizar_frame)

# Controles
def iniciar_live():
    global cap, running
    detener_live()
    cap = cv2.VideoCapture(1)
    running = True
    actualizar_frame()

def detener_live():
    global cap, running
    running = False
    if cap is not None:
        cap.release()
        cap = None
    video_label.configure(image=None)

def seleccionar_video():
    global cap, running
    detener_live()
    path = filedialog.askopenfilename(filetypes=[("Videos", "*.mp4 *.avi *.mov")])
    if path:
        cap = cv2.VideoCapture(path)
        running = True
        actualizar_frame()

def seleccionar_imagen():
    global cap, running
    detener_live()
    path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.png *.jpeg")])
    if path:
        img = cv2.imread(path)
        if img is not None:
            frame = img.copy()
            faces = app.get(frame)

            persona_info = ""
            for face in faces:
                emb = face.embedding
                probs = clf.predict_proba([emb])[0]
                max_prob = np.max(probs)
                # Aqui el pred o la prediccion ya la convierto a entero para que no falle y pueda verificar en la base de datos
                pred = int(np.argmax(probs))

                if max_prob >= THRESHOLD:
                    label = le.inverse_transform([pred])[0]
                    persona = obtener_persona_por_indice(pred)
                    if persona:
                        persona_info += (
                            f"Nombre: {persona['nombre']} {persona['apellido']}\n"
                            f"Identificación: {persona['identificacion']}\n"
                            f"Tipo: {persona['tipo']}\n"
                            f"Fecha de Registro: {persona['fecha_registro']}\n"
                            f"Datos Específicos: {persona['datos_especificos']}\n\n"
                        )
                    else:
                        persona_info += "Persona no encontrada en la base de datos.\n\n"
                else:
                    persona_info += "Reconocimiento facial por debajo del umbral.\n\n"

            info_label.configure(text=persona_info)

            # Mostrar imagen procesada
            frame = detectar_y_mostrar(img)
            frame = cv2.resize(frame, (640, 360))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            img_pil = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img_pil)
            video_label.configure(image=imgtk)
            video_label.image = imgtk

def finalizar():
    detener_live()
    root.destroy()

# Botones
bot_frame = ctk.CTkFrame(root)
bot_frame.pack(pady=10)

ctk.CTkButton(bot_frame, text="Iniciar Live", command=iniciar_live).grid(row=0, column=0, padx=10, pady=10)
ctk.CTkButton(bot_frame, text="Seleccionar Video", command=seleccionar_video).grid(row=0, column=1, padx=10, pady=10)
ctk.CTkButton(bot_frame, text="Seleccionar Imagen", command=seleccionar_imagen).grid(row=0, column=2, padx=10, pady=10)
ctk.CTkButton(bot_frame, text="Detener Live", command=detener_live).grid(row=1, column=0, columnspan=1, pady=10)
ctk.CTkButton(bot_frame, text="Finalizar", command=finalizar).grid(row=1, column=2, columnspan=1, pady=10)

# Información de persona
info_label = ctk.CTkLabel(root, text="", anchor="w", justify="left")
info_label.pack(pady=10)

root.mainloop()

