# camera.py
import time

def detect_faces():
    while True:
        try:
            with open("static/test.jpg", "rb") as f:
                frame_bytes = f.read()
        except Exception:
            frame_bytes = b''

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(1)