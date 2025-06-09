import customtkinter as ctk
import tkinter.messagebox as messagebox
import joblib
from db.insertions import insertar_persona

# Configuración
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.title("Registro de Personas")
app.geometry("520x500")

# LabelEncoder
label_encoder = joblib.load("face_recognition/embeddings/label_encoder.joblib")
nombres = label_encoder.classes_

# Variables
selected_name = ctk.StringVar()
identificacion_var = ctk.StringVar()
nombre_var = ctk.StringVar()
apellido_var = ctk.StringVar()
carrera_var = ctk.StringVar()
semestre_var = ctk.StringVar()

# Callback al seleccionar persona
def on_select(choice):
    tipo = choice.split("/")[0].lower()
    nombre_completo = choice.split("/")[1]
    nombre, apellido = nombre_completo.split("_", 1)
    nombre_var.set(nombre)
    apellido_var.set(apellido)
    if tipo == "estudiante":
        entry_carrera.configure(state="normal")
        entry_semestre.configure(state="normal")
    else:
        carrera_var.set("")
        semestre_var.set("")
        entry_carrera.configure(state="disabled")
        entry_semestre.configure(state="disabled")

# Función de registrar
def registrar():
    nombre_label = selected_name.get()
    if not nombre_label:
        messagebox.showerror("Error", "Selecciona una persona del dataset.")
        return

    tipo = nombre_label.split("/")[0].lower()
    embedding_index = list(nombres).index(nombre_label)

    identificacion = identificacion_var.get().strip()
    nombre = nombre_var.get().strip()
    apellido = apellido_var.get().strip()

    datos_especificos = None
    if tipo == "estudiante":
        carrera = carrera_var.get().strip()
        semestre = semestre_var.get().strip()
        if not carrera or not semestre:
            messagebox.showerror("Error", "Ingresa carrera y semestre.")
            return
        datos_especificos = {"carrera": carrera, "semestre": semestre}

    if not identificacion or not nombre or not apellido:
        messagebox.showerror("Error", "Todos los campos obligatorios deben estar llenos.")
        return

    success, msg = insertar_persona(tipo, identificacion, nombre, apellido, datos_especificos, embedding_index)
    if success:
        messagebox.showinfo("Éxito", msg)
    else:
        messagebox.showerror("Error", msg)

# Frame central (como borde visual)
frame = ctk.CTkFrame(app, width=460, height=420, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Título
ctk.CTkLabel(frame, text="Registro de Personas", font=("Arial", 20)).pack(pady=10)

# Selección
ctk.CTkLabel(frame, text="Selecciona una persona:").pack()
ctk.CTkOptionMenu(frame, variable=selected_name, values=list(nombres), command=on_select).pack(pady=5)

# Cédula
ctk.CTkLabel(frame, text="Cédula:").pack()
ctk.CTkEntry(frame, textvariable=identificacion_var, width=300).pack(pady=5)

# Nombre y Apellido (en línea)
row1 = ctk.CTkFrame(frame, fg_color="transparent")
row1.pack(pady=5)
ctk.CTkLabel(row1, text="Nombres").grid(row=0, column=0, padx=5)
ctk.CTkEntry(row1, textvariable=nombre_var, width=180).grid(row=1, column=0, padx=5)
ctk.CTkLabel(row1, text="Apellidos").grid(row=0, column=1, padx=5)
ctk.CTkEntry(row1, textvariable=apellido_var, width=180).grid(row=1, column=1, padx=5)

# Carrera y Semestre (en línea)
row2 = ctk.CTkFrame(frame, fg_color="transparent")
row2.pack(pady=5)
ctk.CTkLabel(row2, text="Carrera (Solo estudiantes)").grid(row=0, column=0, padx=5)
entry_carrera = ctk.CTkEntry(row2, textvariable=carrera_var, width=180, state="disabled")
entry_carrera.grid(row=1, column=0, padx=5)
ctk.CTkLabel(row2, text="Semestre (Solo estudiantes)").grid(row=0, column=1, padx=5)
entry_semestre = ctk.CTkEntry(row2, textvariable=semestre_var, width=180, state="disabled")
entry_semestre.grid(row=1, column=1, padx=5)

# Botón registrar
ctk.CTkButton(frame, text="Registrar", command=registrar).pack(pady=20)

app.mainloop()

