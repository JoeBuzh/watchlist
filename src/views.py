# -*- coding:utf-8 -*-
# @auhtor: Joe-Bu

import os

from flask import url_for, render_template
from flask import request, redirect, flash

from src import app, db
from src.models import User, Movie

from flask_login import login_user, logout_user
from flask_login import login_required, current_user


@app.route('/ty')
def ty():
    return u"欢迎来到田莹的网页！"


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
        # check login
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) > 60:
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
@login_required
def edit(movie_id):
    '''
        Edit Movie List.
    '''
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid Input.')
            return redirect(url_for('edit'), movie_id=movie_id)

        movie.title = title
        movie.year = year
        db.session.add(movie)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    '''
        Delete movie.
    '''
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Delete Item!')
    redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
        Login.
    '''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid Input.')
            return redirect(url_for('login'))

        user = User.query.first()
        if username==user.username and user.valid_password(password):
            login_user(user)
            flash('Login Success!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or passwprd.')
            return redirect(url_for('login'))
    
    return render_template('login.html')    


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Bye!')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name)>20:
            flash('Invalid Name.')
            return redirect(url_for('settings'))

        # current_user.name = name
        user = User.query.first()
        user.name = name
        db.session.commit()
        flash('Setting!')
        return redirect(url_for('index'))

    return render_template('settings.html')