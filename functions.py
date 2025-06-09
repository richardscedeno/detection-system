import os
import cv2
from datetime import datetime
import sys

sys.path.append('./telegram_bot')
from telegram_bot.bot import TelegramBot
from db.insertions import insertar_alerta, insertar_deteccion_arma

bot = TelegramBot(properties_path='./telegram_bot/.telegram_keys')

def notify_last_detection(frame, mensaje=None):
    """
    Guarda el frame con la detección, lo envía a Telegram y lo registra en la base de datos.
    """
    # Crear carpeta si no existe
    directory = "detections"
    os.makedirs(directory, exist_ok=True)

    # Crear nombre único
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{directory}/arma_{timestamp}.jpg"

    # Guardar imagen
    cv2.imwrite(filename, frame)
    print(f"[INFO] Imagen guardada: {filename}")

    # Enviar a Telegram
    if mensaje is None:
        mensaje = "Se detectó un arma en el laboratorio."
        
    # Enviar a Telegram
    bot.send_photo_to_channel(filename, 'Arma detectada')

    # Registro en base de datos
    fecha = datetime.now()
    tipo_arma = "arma" 
    confianza = 0.85  # Valor fijo o puedes pasarlo como argumento si quieres
    ubicacion = "Laboratorio B"

    # Insertar y obtener ID
    arma_id = insertar_deteccion_arma(fecha, tipo_arma, confianza, ubicacion, filename)

    insertar_alerta(tipo=tipo_arma, mensaje=mensaje, fecha_hora_envio=fecha, deteccion_arma_id=arma_id)

    return filename

