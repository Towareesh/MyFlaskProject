from flask import (render_template,
                   redirect,
                   url_for,
                   flash)
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index/')
@app.route('/index')
def index():
    """ Decorated func: index()
        Представление страницы с моделью микроблога.
        Обрабатываемый шаблон index.html наследуется от base.html.

    Returns:
        str: object render_template
    """

    user = {'username': 'Аннушка'}
    posts = [
        {
            'author': {'username': 'Vlad'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Tony'},
            'body': 'Nice mother'
        },
        {
            'author': {'username': 'Mark'},
            'body': 'Bullshit!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/home')
def home():
    """ Decorated func: home() 
        Представление главной страницы.

    Returns:
        str: object render_template
    """

    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Decorated func: login()
        Представление страницы с моделью регистации.
        Обрабатываемый шаблон login.html наследуется от base.html.

    Returns:
        str: object render_template
    """

    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        data = User(form.username.data, form.password.data)
        # print(form.username.data, form.password.data)
        # return redirect(url_for('index'))
    return render_template('login.html', title='Войти', form=form)

