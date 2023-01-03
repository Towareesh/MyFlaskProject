import datetime

from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.forms import EditProfileForm
from app.models import User



@app.route('/')
@app.route('/index/')
@app.route('/index')
@login_required
def index():
    """ Decorated func: index()
        Представление страницы с моделью микроблога.
        Обрабатываемый шаблон index.html наследуется от base.html.

    Returns:
        str: object render_template
    """
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
    return render_template('index.html', title='Home', posts=posts)


@app.route('/home')
def home():
    """ Decorated func: home() 
        Представление главной страницы.

    Returns:
        str: object render_template()
    """

    return render_template('base.html')


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
            {'author': user, 'body': 'Test post_1'},
            {'author': user, 'body': 'Test post_2'}
            ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Decorated func: login()
        Представление страницы с моделью регистации.
        Обрабатываемый шаблон login.html наследуется от base.html.

    Returns:
        str: object render_template
    """

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    now_time = datetime.datetime.now()
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        print(f'user: {form.username.data} - - {now_time.strftime("%d-%m-%Y %H:%M")}')
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Изменения сохранены')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)