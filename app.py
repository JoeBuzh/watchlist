# -*- coding:utf-8 -*-
# @auhtor: Joe-Bu

import os
import click

from flask import Flask
from flask import url_for, render_template
from flask import request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + \
    os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_KEY'] = 'dev'

db = SQLAlchemy(app)

@app.cli.command()
@click.option('--drop', is_flag=True, help='create after drop.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
def forge():
    '''
        Generate fake data
    '''
    db.create_all()

    name = "Joe Bu"
    movies = [
        {'title': '我不是药神', 'year': '2019'},
        {'title': '流感', 'year': '2018'},
        {'title': '铁线虫入侵', 'year': '2018'},
        {'title': '哪吒', 'year': '2019'},
        {'title': '神探狄仁杰', 'year': '2016'},
        {'title': '为爱迫降', 'year': '2020'},
        {'title': '战狼2', 'year': '2017'},
        {'title': '亲爱的，新年好', 'year': '2020'},
    ]
    user = User(name=name)
    db.session.add(user)

    for movie in movies:
        mv = Movie(title=movie['title'], year=movie['year'])
        db.session.add(mv)

    db.session.commit()
    click.echo("Insert Done!")


# tablename: user
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(28))


# tablename: movie
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


'''
@app.route('/')
@app.route('/bzh')
def hello():
    return "Welcome to My Watchlist!"
'''


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
    print(url_for('hello'))  # /
    print(url_for('hello_who', name='bzmlxm'))
    print(url_for('test_url_for'))
    print(url_for('ty', num=5))

    return 'Test Page'


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year)>4 or len(title)>60:
            flash("Invalid input.")            # 显示错误
            return redirect(url_for('index'))  # 重定向
        # save submit data
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('New Item Added!')
        return redirect(url_for('index'))

    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    '''
        Edit Movie List.
    '''
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year)>4 or len(title)>60:
            flash('Invalid Input.')
            return redirect(url_for('edit'), movie_id=movie_id)

        movie.title = title
        movie.year = year
        db.session.add(movie)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['GET', 'POST'])
def delete(movie_id):
    '''
        Delete movie.
    '''
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Delete Item!')
    redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    user = User.query.first()
    return render_template('404.html')


@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user) # 类似全局变量，所有html页面均可使用user


