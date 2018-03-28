# coding=utf-8
import os
import codecs
import subprocess
import sys


crawl_path = "/media/store/paper_data_temp/crawl"
data_path = "/media/store/paper_data_temp/data"


def crawl_by_name(model_name, model_target):
    crawl_file = os.path.join(crawl_path, model_name + ".txt")
    with codecs.open(crawl_file, 'w', 'utf-8') as f:
        f.write(model_name + "|" + model_target)
        pass
    pwd = os.getcwd()
    os.chdir("/home/train/myTrain/scripts/idt-pitaya-serv-opencv/target")
    input_dir = crawl_file
    output_dir = os.path.join(data_path, model_target)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        subprocess.call(("sh", "./run.sh", "ImageCrawlerCli", "-input", input_dir, "-output", output_dir))

    os.chdir(pwd)
    sys.exit(0)


# TODO implement the following functions and run auto_modeling() to start all of them
def split(input_dir):
    pass


def cluster(input_dir):
    pass


def model_build(input_dir):
    pass


def auto_modeling():
    pass
