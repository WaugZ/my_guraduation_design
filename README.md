# my_guraduation_design
## no title
- 这里主要做前端
- 公司有关的代码不会传到这个项目

## 运行
- cd $ROOT_OF_THIS_PROJECT
- 启动数据库
    - FLASK_APP = *** flask db init
    - FLASK_APP = *** flask db migrate -m "**** table"
    - FLASK_APP = *** flask db upgrade
        - FLASK_APP = *** flask db downgrade 如果需要降级
- 启动网页
    - FLASK_APP = *** flask run
    - 加入参数 port **** host **** 如果需要更改host或port