# my_guraduation_design
## no title
- 这里主要做前端，后端为基本交互
- 公司相关代码不会传到这个项目

## 运行
- cd $ROOT_OF_THIS_PROJECT
- 启动虚拟环境flask
    - source activate flask
        - 若未创建虚拟环境 conda create --name flask python=2.7/3.4
        - python 3 env flask 也行（未试验）
    - 首次使用，安装依赖
        - for req in $(cat requirements.txt);do pip install $req;done
- 启动数据库
    - FLASK_APP = *** flask db init
    - FLASK_APP = *** flask db upgrade
    - FLASK_APP = *** flask db migrate
        - FLASK_APP = *** flask db downgrade 如果需要降级
- 启动网页
    - FLASK_APP = *** flask run
    - 加入参数 port *** host *** 如果需要更改host或port

## 开发
- 新增数据库表
    - FLASK_APP = *** flask db migrate -m "*** table"
