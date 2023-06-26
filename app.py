import json

import requests
from flask import Flask, render_template, request




app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sendFrame', methods=['POST'])
def sendFrame():
    frame = request.form['frame']
    # frame = request.json

    data = {'frame': frame}
    headers = {'Content-Type': 'application/json'}
    # response = requests.post('http://192.168.1.25:50007/detect', json=frame, headers=headers)
    response = requests.post('http://192.168.1.25:50007/detect', data=json.dumps(data), headers=headers)


    return response.json()


if __name__ == '__main__':
    app.run(port = 1472)