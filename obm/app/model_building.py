# coding=utf-8
import os
import codecs
import subprocess
import sys


global_prefix = "/home/train/myTrain/scripts/idt-pitaya-serv-scheduler/idt-pitaya-serv-scheduler/shelfDetect/"


def crawl_by_name(input_dir, output_dir):
    pwd = os.getcwd()

    os.chdir("/home/train/myTrain/scripts/idt-pitaya-serv-opencv_local/target")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        subprocess.call(("sh", "./run.sh", "ImageCrawlerCli", "-input", input_dir, "-output", output_dir))

    os.chdir(pwd)


# TODO implement the following functions and run auto_modeling() to start all of them
# TODO to implement the following codes with parameters
def split(input_dir, output_dir):
    subprocess.call(('python', global_prefix + '/testToXML_local.py', '--test_dir', input_dir, '--out_dir', output_dir))
    pass


def cluster(input_dir, output_dir):
    subprocess.call(('python', global_prefix + 'features_cluster_local.py', '--test_dir', input_dir, '--out_dir', output_dir))
    pass


def model_build(input_dir, output_dir, data_count):
    data_source = input_dir
    model_path = output_dir
    subprocess.call(('python', global_prefix + 'genImageSetWithOrderAndResize_local.py',
                     '--source', data_source, '--target', model_path))
    subprocess.call(('python', '/home/train/myTrain/scripts/idt-pitaya-serv-train/init_classify_train_local.py',
                     '--traindir', model_path, '--maxiter', str(data_count * 3),
                     '--snapshot', str(data_count * 3), '--stepsize', str(data_count),
                     '--batchsize', '8', '--rootdir', data_source))
    pass


def auto_modeling(model_name, target_name):
    # subprocess.call(('source activate', 'root'))
    crawl_path = "/media/store/paper_data_temp/crawl"
    data_path = "/media/store/paper_data_temp/data"
    model_path = "/media/store/paper_data_temp/models"
    # ---------------- crawl ----------------------------------
    crawl_file = os.path.join(crawl_path, model_name + ".txt")
    with codecs.open(crawl_file, 'w', 'utf-8') as f:
        f.write(target_name + "|" + target_name)
        pass
    crawl_output = os.path.join(data_path, target_name)
    crawl_by_name(crawl_file, crawl_output)
    # ---------------------------------------------------------

    # ---------------- split ---------------------------------
    # the input of split is crawl output
    split_output = os.path.join(data_path, target_name + "_split")
    split(crawl_output, split_output)
    # -------------------------------------------------------

    # ---------------- cluster -------------------------------
    # the input of cluster is split output
    cluster_output = os.path.join(data_path, target_name + "_cluster")
    cluster(split_output, cluster_output)
    # ---------------------------------------------------------

    # -------------------  train ------------------------------
    # the input of train is cluster output
    if not os.path.exists(cluster_output):
        cluster_output = split_output
    data_count = 0;
    for _, _, files in os.walk(cluster_output):
        for file in files:
            data_count += 1
    model_output = os.path.join(model_path, model_name)

    if data_count > 100:
        model_build(cluster_output + '/', model_output, data_count)
    # ---------------------------------------------------------
    sys.exit(0)
    pass
