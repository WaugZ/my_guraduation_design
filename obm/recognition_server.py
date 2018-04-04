# coding=utf-8
import cv2
import os.path as osp
import subprocess
import json
from flask import Flask, request
from lxml import etree
from config import ServerConfig

app = Flask(__name__)

def recognize(model_path, img_name):
    img_base = ServerConfig.UPLOADED_PHOTOS_DEST
    img_path = osp.join(img_base, img_name)
    subprocess.call(('python', ServerConfig.RECOGNITION_SCRIPT_PATH, '--model_path', model_path + '/model',
                     '--img_path', img_path, '--out_path', ServerConfig.RECOGNITION_RESULT_DEST))

    xml = osp.join(ServerConfig.RECOGNITION_RESULT_DEST, 'Annotations', img_name.replace(img_name.split('.')[-1], 'xml'))
    result = {}
    if osp.exists(xml):

        annotation = etree.parse(xml).getroot()
        for object in annotation.iter('object'):
            name = object.find('name').text
            if object.find('desc') is not None:
                name = object.find('desc').text
                print name
            confidence = object.find('confidence').text
            if name in result:
                if confidence > result[name]:
                    result[name] = confidence
            else:
                result[name] = confidence

    max_confidence = 0
    max_label = ""
    for name in result:
        if result[name] > max_confidence:
            max_confidence = result[name]
            max_label = name
    return max_label, max_confidence


@app.route('/', methods=['POST'])
@app.route('/recognition', methods=['POST'])
def recognition():
    # print request.headers
    # print request.form
    model_path = request.form['model_path']
    img_name = request.form['img_name']
    label, confidence = recognize(model_path, img_name)
    j = {"label": label, "confidence": confidence}
    return json.dumps(j)


if __name__ == "__main__":
    app.run(port=9998, debug=True)
