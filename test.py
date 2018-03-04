from flask import Flask, url_for, render_template
from config import DevConfig


app = Flask(__name__)


@app.route('/')
@app.route('/home/')
def home():
    return render_template('home.html')


@app.route('/login/')
def login():
    return render_template('login_notuse.html')


# @app.route('/hello/')
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('hello_notuse.html', name=name)


if __name__ == '__main__':
    app.config.from_object(DevConfig)
    app.run(host='0.0.0.0', port=8080)
