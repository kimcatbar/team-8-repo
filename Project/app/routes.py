from app import myapp_obj, db
from flask_babel import _
from flask import render_template, redirect, url_for, flash, request
from app.forms import LoginForm, RegistrationForm, PostForm
from app.models import User, Post, Comment
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from uuid import uuid4
import os

@myapp_obj.route('/')                                         # default route
def home():
    if current_user.is_authenticated:                         # if user is logged in, return to user home page/dashboard
        return render_template('dashboard.html')
    return render_template('index.html')                      # otherwise, show the splash page


@myapp_obj.route('/login', methods=['GET', 'POST'])           # when a user logs in it checks with the database if the user exists
def login():
    form = LoginForm()                                                                  # log in form
    if form.validate_on_submit():                                                       # check if form is submitted
        current_user = User.query.filter_by(username=form.username.data).first()        # match username with the one entered in the form
        if current_user:
            if check_password_hash(current_user.password, form.password.data):          # check if the password matches
                login_user(current_user, remember=form.remember_me.data)                # log in if it does, keeping in mind if the user login wants to be remembered
                return redirect(url_for('dashboard'))                                   # redirect to user home page
    return render_template('login.html', form=form)                                     # otherwise, return back to log in page if it failed

@myapp_obj.route('/dashboard', methods=['GET', 'POST'])                                 # user home page
@login_required
def dashboard():
    form = PostForm()  
    picture_name=None                                                                 # form for making a post
    if form.validate_on_submit():                                                       # check if form is submitted
        if form.image.data:                                                             # if there is an image submitted
            picture = form.image.data
            picture_name = uuid4() + picture.filename                                   # use uuid to make file name unique from other possible duplicates
            pic_path = os.path.join(myapp_obj.root_path, 'static\images', picture_name) # set the path of the image to a local folder in the project
            picture.save(pic_path)                                                      # save the picture at the specified path
        post = Post(body=form.post.data,author=current_user,image=picture_name)         # set post parameters
        db.session.add(post)                                                            # add post to database
        db.session.commit()                                                             # commit changes to database
        flash("Your post is live!")
        return redirect(url_for('dashboard'))                                           # redirect back to user home page
    posts = current_user.my_posts().all()
    return render_template('dashboard.html',form=form,posts=posts)                      # return to user home page

@myapp_obj.route('/logout', methods=['GET', 'POST'])                 # logout
@login_required
def logout():
    logout_user()                                                    # log out the user
    return redirect('/')                                             # redirect back to splash page


@myapp_obj.route('/register', methods=['GET', 'POST'])                                  # register page
def register():
    form = RegistrationForm()                                                           # registration form
    if form.validate_on_submit():                                                       # validate form submission
        hashed_password = generate_password_hash(form.password.data)                    # generate pw hash to submitted pw
        new_user = User(username=form.username.data, password=hashed_password)          # create a new user
        db.session.add(new_user)                                                        # add new user to database
        db.session.commit()                                                             # commit the changes
        return redirect(url_for('login'))                                               # redirect to log in page

    return render_template('register.html', form=form)

@myapp_obj.route('/delete', methods=['GET', 'POST'])                                    # route to delete account
@login_required
def delete():
    current_user.remove()                                                               # remove the current user
    db.session.commit()                                                                 # commit the changes
    flash(_("Account has been deleted."))                                               
    return redirect('/')                                                                # redirect to splash page

@myapp_obj.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html')                                             # route to settings page

@myapp_obj.route('/messages', methods=['GET', 'POST'])                                  # route to messages
@login_required
def messages():
    return render_template('messages.html')

@myapp_obj.route('/profile', methods=['GET', 'POST'])                                   # route to profile
@login_required
def profile():
    user = current_user                                                                 # set the user
    posts = user.posts.order_by(Post.timestamp.desc())                                  # display the user posts by order of timestamp
    return render_template('profile.html', user=user, posts=posts)

@myapp_obj.route('/user/<username>', methods=['GET','POST'])                            # route to other users' profiles 
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()                      # check if user exists
    posts = user.posts.order_by(Post.timestamp.desc())                                 # display the user posts by order of timestamp
    if username == current_user.username:                                              # if the selected user profile is the current logged in user, redirect to own profile
        return redirect('/profile')
    return render_template('profile.html', user=user,posts=posts)

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
    return redirect(request.referrer)
