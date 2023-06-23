import requests
from flask import Flask, request, render_template
import pickle


import base64
from PIL import Image
import json
import tensorflow as tf
import io
from tf2_yolov4.anchors import YOLOV4_ANCHORS
from tf2_yolov4.model import YOLOv4

app = Flask(__name__)




WIDTH, HEIGHT = (640, 480)

model = YOLOv4(
    input_shape=(HEIGHT, WIDTH, 3),
    anchors=YOLOV4_ANCHORS,
    num_classes=80,
    training=False,
    yolo_max_boxes=50,
    yolo_iou_threshold=0.5,
    yolo_score_threshold=0.5,
)
model.load_weights('yolov4.h5')

CLASSES = [
        'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck',
        'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench',
        'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra',
        'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
        'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
        'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork',
        'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli',
        'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant',
        'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
        'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book',
        'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
    ]
@app.route('/detect', methods=['POST'])
def detect_objects():
    image_data = request.get_json()
    print(image_data)
    # image_data = json.dumps(img_data)
    # image_data = request.form['frame']
    image_data = image_data.replace('data:image/jpeg;base64,', '')


    image_bytes = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_bytes))
    # image.show()

    image = image.resize((WIDTH, HEIGHT))

    image = tf.expand_dims(image, axis=0) / 255

    # image_array = np.frombuffer(image_bytes, np.uint8)
    # image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)


    # run model
    boxes, scores, classes, detections = model.predict(image)

    # create response
    boxes = boxes[0] * [WIDTH, HEIGHT, WIDTH, HEIGHT]
    scores = scores[0]
    classes = classes[0].astype(int)
    detections = detections[0]

    # convert coordinates to a JSON-serializable format
    objects = []
    labels = []
    for (xmin, ymin, xmax, ymax), score, class_idx in zip(boxes, scores, classes):
        if score > 0:
            label = CLASSES[class_idx]+' '+ str(round(score, 2))
            if label in labels:
                continue
            else:
                labels.append(label)
                x1, y1, x2, y2 = int( xmin ), int( ymin ), int( xmax ), int( ymax )
                object_data = {'label': label, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
                objects.append( object_data )


    response_data = {'objects': objects}
    # print(objects)
    # return response
    return json.dumps( response_data )



if __name__ == '__main__':
    app.run(port = 1407)