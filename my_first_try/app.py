#coding=utf-8
from flask import Flask, request, render_template
from flask_login import LoginManager, UserMixin
from config import DevConfig

app = Flask(__name__)
#用户认证
login_manger=LoginManager()
#配置用户认证信息
login_manger.init_app(app)
#认证加密程度
login_manger.session_protection='strong'
#登陆认证的处理视图
login_manger.login_view='auth.login'
#登陆提示信息
login_manger.login_message=u'对不起，您还没有登录'
login_manger.login_message_category='info'

#用户表
# class Users(db.Model,UserMixin):
#     __tablename__='users'
#     id=db.Column(db.Integer,primary_key=True)
#     username=db.Column(db.String(20),nullable=False,index=True)
#     password=db.Column(db.String(255), nullable=False,index=True)
#     phone=db.Column(db.String(32),nullable=False)
#     email=db.Column(db.String(50),nullable=False)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/signin/', methods=['GET'])
def signin_form():
    return render_template('form.html')


@app.route('/signin/', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    if username is 'admin' and password is 'password':
        return render_template('signin-ok.html', username=username)
    return render_template('form.html', message='Bad username or password', username=username)

if __name__ == '__main__':
    app.config.from_object(DevConfig)
    app.run(host="0.0.0.0", port=8080)


