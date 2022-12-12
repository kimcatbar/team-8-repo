from app import myapp_obj, db
from flask import render_template, redirect, url_for, flash, request
from app.forms import LoginForm, RegistrationForm, PostForm
from app.models import User, Post, Comment
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

@myapp_obj.route('/')
def home():
    return render_template('home.html')


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


@myapp_obj.route('/dashboard', methods=['GET', 'POST'])#display text box and posts in dashboard           
@login_required
def dashboard():
    form = PostForm()#uses form format from models 
    if form.validate_on_submit():#if all requriements for post are met
        print("forms" + form.post.data)
        post = Post(body=form.post.data,user_id=current_user.id)#text post is created
        db.session.add(post)#post staged
        db.session.commit()#post is added to databse 
        flash('Your post in live!')
        return redirect(url_for('dashboard'))#redirected and displayed to dashboard 
    posts = current_user.my_posts().all()#display user's posts
    return render_template('dashboard.html', title="Home Page",form=form,posts=posts)


@myapp_obj.route('/logout', methods=['GET', 'POST'])                 #logout form
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


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
    flash("Account has been deleted.")
    return redirect('/home')

@myapp_obj.route('/user/<username>', methods=['GET','POST'])#user profile page
@login_required
def profile(username):
    form = PostForm()#form used to user can sumbit a post
    if form.validate_on_submit():
        print("forms" + form.post.data)
        post = Post(body=form.post.data,user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post in live!')
        return redirect(url_for('profile',username=username))#post and redirect to user profile
    posts = current_user.my_posts().all()#display all user posts in profile
    return render_template('user_profile.html', form = form, posts=posts)
  
@myapp_obj.route("/create-comment/<post_id>", methods = ['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')
    if not text:
        flash('Comment cannot be empty', category = 'error')
    else:
       post = Post.query.filter_by(id=post_id)
       if post:
            comment = Comment(body=text, user_id=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()  
    return redirect(url_for("dashboard"))




