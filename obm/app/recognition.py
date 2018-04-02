# coding=utf-8
import cv2
import os.path as osp
import subprocess
from lxml import etree
from config import Config


def recognize(model_path, img_name):
    img_base = Config.UPLOADED_PHOTOS_DEST
    img_path = osp.join(img_base, img_name)
    subprocess.call(('python', Config.RECOGNITION_SCRIPT_PATH, '--model_path', model_path + '/model',
                     '--img_path', img_path, '--out_path', Config.RECOGNITION_RESULT_DEST))

    xml = osp.join(Config.RECOGNITION_RESULT_DEST, 'Annotations', img_name.replace(img_name.split('.')[-1], 'xml'))
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
