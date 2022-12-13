from app import myapp_obj, db
from flask import render_template, redirect, url_for, flash, request, abort
from app.forms import LoginForm, RegistrationForm, EmptyForm
from app.models import User, Message, Post
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import MessageForm


@myapp_obj.route('/home',methods=['GET', 'POST'] )
@myapp_obj.route('/',methods=['GET', 'POST'] )
def home():
    return render_template("home.html")


@myapp_obj.route('/login', methods=['GET', 'POST'])           #when a user logs in it checks with the database if the user exists
def login():
    form = LoginForm()
    if form.validate_on_submit():
        current_user = User.query.filter_by(username=form.username.data).first()
        if current_user:
            if check_password_hash(current_user.password, form.password.data):
                login_user(current_user, remember=form.remember_me.data)
                return render_template('dashboard.html', user=current_user)

    return render_template('login.html', form=form)


@myapp_obj.route('/dashboard', methods=['GET', 'POST'])              
@login_required
def dashboard():
    return render_template('dashboard.html', user=user)


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

#this is to create the follow user
@myapp_obj.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username): #define the follow function to let the user can follow another user
    form = EmptyForm()
    if form.validate_on_submit(): #this get error when user enter incorrect another user's account
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user: #this will stop user to follow themself
            flash('Try again. You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

#this helps user can unfollow their followed
@myapp_obj.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit(): #this appears when the account user found doesn't exist
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            flash('User {} not found.'.format(username.data))
            return redirect(url_for('index'))
        if user == current_user:  #this appears when the user follow themselves
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username.data))
        current_user.unfollow(user)
        db.session.commit()       #this appears the one user is following
        flash('You are not following {}.'.format(username.data))
        return redirect(url_for('user', username=username.data))
    else:
        return redirect(url_for('index'))

@myapp_obj.route('/user/<username>/following') #this is to show who are following the user's acc
def showFollowing():
	user = getUser()
	return render_template('userList.html', users = user.following()) #link to the userList.html

@myapp_obj.route('/user/<username>/followers') #this is to show who user is currently following
def showFollowers():
	user = getUser()
	return render_template('userList.html', users = user.followers()) ##link to the userList.html

def getUser(username):
	try:
		return User.get(User.username == username)
	except User.DoesNotExist:
		abort(404)

@myapp_obj.route('/user/<username>')
@login_required
def user(username):
    form = EmptyForm()
    return render_template('user.html', user=user, form=form)

@myapp_obj.route('/', methods=['GET', 'POST']) 
@myapp_obj.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = EmptyForm()   
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page=page, per_page=myapp_obj.config['POSTS_PER_PAGE'], error_out=False)
    return render_template('index.html', title='Home', form=form,
                           posts=posts.items)

#the user can send the private message
@myapp_obj.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        mes = send_message(user=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(mes)
        db.session.commit()
        flash(('Your message has been sent.'))          
        return redirect(url_for('user', username=recipient))
    return render_template('send_message.html', title=('Send Message'),
                           form=form, recipient=recipient)

