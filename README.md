# my_guraduation_design
## no title
- 这里主要做前端，后端为基本交互
- 公司相关代码(核心服务器)不会传到这个项目

## 运行
- cd obm
- 启动虚拟环境flask
    - source activate flask
        - 若未创建虚拟环境 conda create --name flask python=2.7/3.4
        - python 3 env flask 也行（未试验）
        - 若不会污染其他python程序的依赖包，也可以不使用虚拟环境
    - 首次使用，安装依赖
        - for req in $(cat requirements.txt);do pip install $req;done
- 启动数据库
    - FLASK_APP=obm flask db init
    - FLASK_APP=obm flask db upgrade
    - FLASK_APP=obm flask db migrate
        - FLASK_APP=obm flask db downgrade 如果需要降级
- 启动网页
    - FLASK_APP=obm flask run
    - 加入参数 port *** host *** 如果需要更改host或port

## 开发
- 新增数据库表
    - FLASK_APP=obm flask db migrate -m "*** table"

- 一些快速启动脚本
    - start_db.sh
        - 包含db init upgrade migrate 保证数据库更新（内容和列）
    - obm_debug.sh
        - （开发用） 含有**debug功能**的启动网页服务器
    - obm_devserver.sh
        - （正式用） 启动网页服务器

## 核心服务器
- 建模服务器
    - python model_build_server.py 启动建模服务器

- 识别服务器
    - python recognition_server.py 启动识别服务器、
