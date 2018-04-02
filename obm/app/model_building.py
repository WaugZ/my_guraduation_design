# coding=utf-8
import os
import codecs
import subprocess
import sys
from datetime import datetime
from config import Config


def crawl_by_name(input_dir, output_dir):
    pwd = os.getcwd()

    os.chdir(Config.CRAWL_SCRIPT_PATH)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        subprocess.call(("sh", "./run.sh", "ImageCrawlerCli", "-input", input_dir, "-output", output_dir))

    os.chdir(pwd)


# TODO implement the following functions and run auto_modeling() to start all of them
# TODO to implement the following codes with parameters
def split(input_dir, output_dir):
    subprocess.call(('python', Config.SPLIT_SCRIPT_PATH, '--test_dir',input_dir, '--out_dir', output_dir))
    pass


def cluster(input_dir, output_dir):
    subprocess.call(('python', Config.CLUSTER_SCRIPT_PATH, '--test_dir', input_dir, '--out_dir', output_dir))
    pass


def model_build(input_dir, output_dir, data_count):
    data_source = input_dir
    model_path = output_dir
    subprocess.call(('python', Config.DATA_GEN_SCRIPT_PATH,
                     '--source', data_source, '--target', model_path))
    subprocess.call(('python', Config.TRAIN_SCRIPT_PATH,
                     '--traindir', model_path, '--maxiter', str(data_count * 3),
                     '--snapshot', str(data_count * 3), '--stepsize', str(data_count),
                     '--batchsize', '8', '--rootdir', data_source))
    pass


def auto_modeling(model_name, target_names):
    # subprocess.call(('source activate', 'root'))
    crawl_path = Config.CRAWL_PATH
    data_path = Config.DATA_PATH
    model_path = Config.MODEL_PATH
    model_name = model_name
    # ---------------- crawl ----------------------------------
    crawl_output = os.path.join(data_path, model_name)
    crawl_file = os.path.join(crawl_path, model_name + ".txt")
    target_names = target_names.split('#')
    with codecs.open(crawl_file, 'w', 'utf-8') as f:
        for target_name in target_names:
            f.write(target_name + "|" + target_name + '\n')
        pass

    crawl_by_name(crawl_file, crawl_output)
    # ---------------------------------------------------------

    # ---------------- split ---------------------------------
    # the input of split is crawl output
    split_output = os.path.join(data_path, model_name + "_split")
    split(crawl_output, split_output)
    # -------------------------------------------------------

    # ---------------- cluster -------------------------------
    # the input of cluster is split output
    cluster_output = os.path.join(data_path, model_name + "_cluster")
    cluster(split_output, cluster_output)
    # ---------------------------------------------------------

    # -------------------  train ------------------------------
    # the input of train is cluster output
    if not os.path.exists(cluster_output):
        cluster_output = split_output
    data_count = 0
    for _, _, files in os.walk(cluster_output):
        for file in files:
            data_count += 1
    model_output = os.path.join(model_path, model_name)

    if data_count > 100:
        model_build(cluster_output + '/', model_output, data_count)
    # ---------------------------------------------------------
    sys.exit(0)
    pass
