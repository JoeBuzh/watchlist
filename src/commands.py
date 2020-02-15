# -*- coding:utf-8 -*-
# @auhtor: Joe-Bu

import click

from src import app, db
from src.models import User, Movie


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


@app.cli.command()
@click.option('--username', prompt=True, help='Login username')
@click.option('--password', prompt=True, hide_input=True,
              confirmation_prompt=True, help='Login password')
def admin(username, password):
    db.create_all()

    user = User.query.first()
    if user.name == 'admin':
        click.echo('Updating user ...')
        user.username = username
        user.set_password(password)
    elif user.name != 'admin':
        click.echo('Renaming user ...')
        user.name = 'admin'
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user ...')
        user = User(username=username, name='admin')
        user.set_password(password)
        db.session.add(user)
    
    db.session.commit()
    click.echo('Done!')