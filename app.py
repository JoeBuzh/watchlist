# -*- coding:utf-8 -*-
# @auhtor: Joe-Bu

from flask import Flask
from flask import url_for

app = Flask(__name__)

@app.route('/')
@app.route('/bzh')
def hello():
    return "Welcome to My Watchlist!"

@app.route('/bzh')
def bzh():
    return u'欢迎来到卜泽昊的网页！'

@app.route('/user/<name>')
def hello_who(name):
    return u'你好{0}'.format(name)

@app.route('/ty')
def ty():
    return u"欢迎来到田莹的网页！"

@app.route('/img')
def image():
    return '<h1>Hello World!</h1><img src="http://helloflask.com/totoro.gif">'

# web <- return cmd <- print
@app.route('/test')
def test_url_for():
    print(url_for('hello')) # /
    print(url_for('hello_who', name='bzmlxm'))
    print(url_for('test_url_for'))
    print(url_for('ty', num=5))

    return 'Test Page'