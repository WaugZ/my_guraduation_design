# coding=utf-8
import cv2
import os.path as osp
import subprocess
from config import Config


def recognize(model_path, img_name):
    img_base = Config.UPLOADED_PHOTOS_DEST
    img_path = osp.join(img_base, img_name)
    subprocess.call(('python', Config.RECOGNITION_SCRIPT_PATH, '--model_path', model_path + '/model',
                     '--img_path', img_path, '--out_path', Config.RECOGNITION_RESULT_DEST))


