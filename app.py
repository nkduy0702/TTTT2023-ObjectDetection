import json
import pickle

import requests
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sendFrame', methods=['POST'])
def sendFrame():
    frame = request.form['frame']
    # print(frame)
    # image_data = { 'Frame': frame }
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://127.0.0.1:1407/detect', json=frame, headers=headers)

    print(response.json())
    return response.json()





if __name__ == '__main__':
    app.run(port = 1472)