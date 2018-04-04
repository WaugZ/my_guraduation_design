# coding=utf-8
from flask import Flask, request
import os
import codecs
import subprocess
import psutil
from multiprocessing import Process
from config import ServerConfig

app = Flask(__name__)   # 创建一个wsgi应用


def crawl_by_name(input_dir, output_dir):
    pwd = os.getcwd()

    os.chdir(ServerConfig.CRAWL_SCRIPT_PATH)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        subprocess.call(("sh", "./run.sh", "ImageCrawlerCli", "-input", input_dir, "-output", output_dir))

    os.chdir(pwd)


def split(input_dir, output_dir):
    subprocess.call(('python', ServerConfig.SPLIT_SCRIPT_PATH, '--test_dir',input_dir, '--out_dir', output_dir))
    pass


def cluster(input_dir, output_dir):
    subprocess.call(('python', ServerConfig.CLUSTER_SCRIPT_PATH, '--test_dir', input_dir, '--out_dir', output_dir))
    pass


def model_build(input_dir, output_dir, data_count):
    data_source = input_dir
    model_path = output_dir
    subprocess.call(('python', ServerConfig.DATA_GEN_SCRIPT_PATH,
                     '--source', data_source, '--target', model_path))
    subprocess.call(('python', ServerConfig.TRAIN_SCRIPT_PATH,
                     '--traindir', model_path, '--maxiter', str(data_count * 3),
                     '--snapshot', str(data_count * 3), '--stepsize', str(data_count),
                     '--batchsize', '8', '--rootdir', data_source))
    pass


def auto_modeling(model_name, target_names):
    # subprocess.call(('source activate', 'root'))
    crawl_path = ServerConfig.CRAWL_PATH
    data_path = ServerConfig.DATA_PATH
    model_path = ServerConfig.MODEL_PATH
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
    pass


@app.route('/', methods=['POST'])
@app.route('/build', methods=['POST'])
def model_building():
    # print request.headers
    # print request.form
    name = request.form['name']
    targets = request.form['targets']
    p = Process(target=auto_modeling, args=(name, targets, ))
    p.daemon = True
    p.start()
    # auto_modeling(name, targets)
    # print request.form.get('name')
    # print request.form.getlist('name')
    # print request.form.get('target')
    return 'Model on construct'


@app.route('/check', methods=['POST'])
def check():
    path = request.form['model_path']
    # return path
    if os.path.exists(os.path.join(path, 'model')):
        for parent, _, files in os.walk(os.path.join(path, 'model')):
            for f in files:
                if f.endswith('.caffemodel'):
                    return "complete"

    return "no"


if __name__ == '__main__':
    app.run(port=9999, debug=True)      #启动app的调试模式