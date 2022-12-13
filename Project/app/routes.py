from app import myapp_obj, db
from flask_babel import _, lazy_gettext
from flask import render_template, redirect, url_for, flash, request
from app.forms import LoginForm, RegistrationForm, PostForm, EmptyForm
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
    form = PostForm()                                                                   # form for making a post
    picture_name = None
    if form.validate_on_submit():                                                       # check if form is submitted
        if form.image.data:                                                             # if there is an image submitted
            picture = form.image.data
            picture_name = str(uuid4()) + picture.filename                                   # use uuid to make file name unique from other possible duplicates
            pic_path = os.path.join(myapp_obj.root_path, 'static\images', picture_name) # set the path of the image to a local folder in the project
            picture.save(pic_path)                                                      # save the picture at the specified path
        post = Post(body=form.post.data,author=current_user,image=picture_name)         # set post parameters
        db.session.add(post)                                                            # add post to database
        db.session.commit()                                                             # commit changes to database
        flash(_("Your post is live!"))
        return redirect(url_for('dashboard'))                                           # redirect back to user home page
    posts = current_user.followed_posts()
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

@myapp_obj.route('/user/<username>', methods=['GET','POST'])                            # route to other users' profiles 
@login_required
def userProfile(username):
    user = User.query.filter_by(username=username).first_or_404()                      # check if user exists
    posts = user.posts.order_by(Post.timestamp.desc())                                 # display the user posts by order of timestamp
    form = EmptyForm()
    return render_template('profile.html', user=user,posts=posts, form=form)

@myapp_obj.route("/create-comment/<post_id>", methods = ['POST'])                       # route to create a comment
@login_required
def create_comment(post_id):                                                            # using HTML form to get text
    text = request.form.get('text')
    if not text:
        flash(_('Comment cannot be empty'), category = 'error')                         # error if no text
    else:
       post = Post.query.filter_by(id=post_id)                                          # find the corresponding post
       if post:
            comment = Comment(body=text, user_id=current_user.id, post_id=post_id)      # set comment values and add it, then commit to database
            db.session.add(comment)
            db.session.commit()  
    return redirect(request.referrer)                                                   # redirect to original location

@myapp_obj.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username): #define the follow function to let the user can follow another user
    form = EmptyForm()
    if form.validate_on_submit(): #this get error when user enter incorrect another user's account
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(lazy_gettext('User %(username)s not found.', username=username))
            return redirect(request.referrer)
        if user == current_user: #this will stop user to follow themself
            flash(_('Try again. You cannot follow yourself!'))
            return redirect(url_for('userProfile', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(lazy_gettext('You are following %(username)s!', username=username))
        return redirect(url_for('userProfile', username=username))
    else:
        return redirect(request.referrer)

#this helps user can unfollow their followed
@myapp_obj.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit(): #this appears when the account user found doesn't exist
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(lazy_gettext('User %(username)s not found.', username=username))
            return redirect(request.referrer)
        if user == current_user:  #this appears when the user follow themselves
            flash(_('You cannot unfollow yourself!'))
            return redirect(url_for('userProfile', username=username))
        current_user.unfollow(user)
        db.session.commit()       #this appears the one user is following
        flash(lazy_gettext('You have unfollowed %(username)s.', username=username))
        return redirect(url_for('userProfile', username=username))
    else:
        return redirect(request.referrer)

@myapp_obj.route('/user/<username>/following') #this is to show who are following the user's acc
def showFollowing(username):
	user = User.query.filter_by(username=username).first()
	return render_template('userFollowing.html', users = user.followed.all()) #link to the userList.html

@myapp_obj.route('/user/<username>/followers') #this is to show who user is currently following
def showFollowers(username):
	user = User.query.filter_by(username=username).first()
	return render_template('userFollowers.html', users = user.followers.all()) ##link to the userList.html
