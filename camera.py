# camera.py
import cv2
import os
from datetime import datetime
from bot import send_face_detected
import asyncio  # <-- добавлено

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
PHOTOS_DIR = "detected_faces"

os.makedirs(PHOTOS_DIR, exist_ok=True)

bot_app_ref = None

def set_bot_app(bot_app):
    global bot_app_ref
    bot_app_ref = bot_app

def detect_faces():
    cap = cv2.VideoCapture(0)  # 0 - основная камера
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(faces) > 0:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            photo_path = os.path.join(PHOTOS_DIR, f"{timestamp}.jpg")
            cv2.imwrite(photo_path, frame)
            if bot_app_ref:
                asyncio.run_coroutine_threadsafe(send_face_detected(bot_app_ref), bot_app_ref.bot.loop)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')