#coding=utf-8
from flask import Flask, request, render_template
from flask_login import LoginManager, UserMixin
from config import DevConfig

app = Flask(__name__)
login_manager = LoginManager()
login_manager.session_protection = "strong"

# 可设置为None，basic，strong已提供不同的安全等级
# login_manager.login_view = "login"  # 设置登录页


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


