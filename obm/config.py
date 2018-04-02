import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # ADMINS = ['your-email@example.com']
    LANGUAGES = ['en', 'es']
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    # POSTS_PER_PAGE = 25
    MODEL_PER_PAGE = 10

    # some path for data saving
    UPLOADED_PHOTOS_DEST = os.path.join(os.getcwd(), 'temp_img')
    RECOGNITION_RESULT_DEST = os.path.join(os.getcwd(), 'temp_xml')
    CRAWL_PATH = "/media/store/paper_data_temp/crawl"
    DATA_PATH = "/media/store/paper_data_temp/data"
    MODEL_PATH = "/media/store/paper_data_temp/models"
    CRAWL_SCRIPT_PATH = "/home/train/myTrain/scripts/idt-pitaya-serv-opencv_local/target"
    SPLIT_SCRIPT_PATH = "/home/train/myTrain/scripts/idt-pitaya-serv-scheduler/idt-pitaya-serv-scheduler/shelfDetect/testToXML_local.py"
    CLUSTER_SCRIPT_PATH = "/home/train/myTrain/scripts/idt-pitaya-serv-scheduler/idt-pitaya-serv-scheduler/shelfDetect/features_cluster_local.py"
    DATA_GEN_SCRIPT_PATH = "/home/train/myTrain/scripts/idt-pitaya-serv-scheduler/idt-pitaya-serv-scheduler/shelfDetect/genImageSetWithOrderAndResize_local.py"
    TRAIN_SCRIPT_PATH = "/home/train/myTrain/scripts/idt-pitaya-serv-train/init_classify_train_local.py"
    RECOGNITION_SCRIPT_PATH = "/home/train/myTrain/scripts/idt-pitaya-serv-scheduler/idt-pitaya-serv-scheduler/shelfDetect/shelfDetection_local.py"
