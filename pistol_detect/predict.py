import cv2
from ultralytics import YOLO

if __name__ == '__main__':
    img_name = 'test2.jpg'
    img = cv2.imread(f'./data/{img_name}')

    model = YOLO('./weights/best50.pt')

    pred = model.predict(img)[0]
    pred = pred.plot()

    cv2.imwrite(f'./predict/{img_name}', pred)
