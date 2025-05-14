# web.py
from flask import Flask, Response, render_template, send_from_directory
import os

# Импортируем функцию из camera.py
from camera import detect_faces

app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    return Response(detect_faces(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    photos = []
    for filename in sorted(os.listdir("detected_faces"), reverse=True):
        if filename.endswith(".jpg"):
            photos.append(filename)
    return render_template('index.html', photos=photos)

@app.route('/detected_faces/<filename>')
def uploaded_file(filename):
    return send_from_directory("detected_faces", filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)