import cv2
#import imutils
from ultralytics import YOLO
#import functions

model = YOLO('../weights/best70.pt')

video_path = "./data/vid4.mp4"
cap = cv2.VideoCapture(video_path)

# Tamaño deseado para la ventana de visualización
window_width = 800
window_height = 600

# Crear la ventana con tamaño fijo
cv2.namedWindow("YOLOv8", cv2.WINDOW_NORMAL)
cv2.resizeWindow("YOLOv8", window_width, window_height)

while cap.isOpened():
    success, frame = cap.read()

    if not success:
        break

    # Copia para procesamiento
    frame_copy = frame.copy()
    
    # Procesamiento con YOLO
    results = model(frame, conf=0.4, save_crop=True)
    
    # Obtener el frame con las detecciones
    plot_frame = results[0].plot()
    
    # Redimensionar manteniendo relación de aspecto
    height, width = plot_frame.shape[:2]
    ratio = min(window_width/width, window_height/height)
    new_width = int(width * ratio)
    new_height = int(height * ratio)
    resized_frame = cv2.resize(plot_frame, (new_width, new_height))
    
    # Mostrar el frame redimensionado
    cv2.imshow("YOLOv8", resized_frame)

    # Verificar confianzas
    conf = results[0].boxes.conf
    if conf.nelement() != 0:
        print(f'Tiene datos: {conf.nelement()}')
        #functions.verify_path()
    else:
        print(f'Está vacio: {conf.nelement()}')

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
