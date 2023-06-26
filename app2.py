import base64
import json

import requests
from flask import Flask, render_template, Response
import cv2
import numpy as np

app = Flask(__name__)
camera = cv2.VideoCapture(0)
color = (0, 255, 0)  # Màu sắc (xanh lá cây)
thickness = 2  # Độ dày viền

WIDTH = 640
HEIGHT = 480
def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Xử lý frame ở đây (nếu cần)
            frame = cv2.resize(frame, (WIDTH, HEIGHT))
            # image = tf.image.resize(frame, (HEIGHT, WIDTH))
            _, img_encoded = cv2.imencode('.jpg', frame)
            image_base64 = base64.b64encode(img_encoded).decode()

            framedata = json.dumps(image_base64)
            headers = {'Content-Type': 'application/json'}
            response = requests.post('http://127.0.0.1:1407/detect', json=framedata, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                objects = response_data['objects']
                for obj in objects:
                    label = obj['label']
                    x1, y1, x2, y2 = obj['x1'], obj['y1'], obj['x2'], obj['y2']
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, thickness)

                print('Image uploaded and processed successfully')
            else:
                print('Error uploading image:', response.text)


            # Chuyển đổi frame thành định dạng JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()



            # Đẩy frame như một Response object
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index2.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(port = 1111)
