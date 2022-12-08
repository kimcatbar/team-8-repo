from app import myapp_obj, db
from flask_babel import _
from flask import render_template, redirect, url_for, flash
from app.forms import LoginForm, RegistrationForm, PostForm
from app.models import User, Post
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
import os

@myapp_obj.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('dashboard.html')
    return render_template('index.html')


@myapp_obj.route('/login', methods=['GET', 'POST'])           #when a user logs in it checks with the database if the user exists
def login():
    form = LoginForm()
    if form.validate_on_submit():
        current_user = User.query.filter_by(username=form.username.data).first()
        if current_user:
            if check_password_hash(current_user.password, form.password.data):
                login_user(current_user, remember=form.remember_me.data)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@myapp_obj.route('/dashboard', methods=['GET', 'POST'])              
@login_required
def dashboard():
    form = PostForm()
    if form.validate_on_submit():
        if form.image.data:
            picture = form.image.data
            picture_name = picture.filename
            pic_path = os.path.join(myapp_obj.root_path, 'static\images', picture_name)
            picture.save(pic_path)
        post = Post(body=form.post.data,author=current_user,image=picture_name)
        db.session.add(post)
        db.session.commit()
        flash("Your post is live!")
        return redirect(url_for('dashboard'))
    posts = [
        {
            'author': {"username": 'antony'},
            "body": "Beautiful day ain't it!"
        }   
    ]
    return render_template('dashboard.html',form=form,posts=posts)


@myapp_obj.route('/logout', methods=['GET', 'POST'])                 #logout form
@login_required
def logout():
    logout_user()
    return redirect('/')


@myapp_obj.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@myapp_obj.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    current_user.remove()
    db.session.commit()
    flash(_("Account has been deleted."))
    return redirect('/home')

@myapp_obj.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html')

@myapp_obj.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    return render_template('messages.html')

@myapp_obj.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = current_user
    posts = user.posts.order_by(Post.timestamp.desc())
    return render_template('profile.html', user=user, posts=posts)

@myapp_obj.route('/user/<username>', methods=['GET','POST'])#profile 
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc())
    if username == current_user.username:
        return redirect('/profile')
    return render_template('profile.html', user=user,posts=posts)