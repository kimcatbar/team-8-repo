
from app import myapp_obj, db
from flask import render_template, redirect, url_for, flash
from app.forms import LoginForm, RegistrationForm
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask import Flask, render_template, request, make_response
import sqlite3

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


@myapp_obj.route('/dashboard', methods=['GET', 'POST'])              
@login_required
def dashboard():
    
    return render_template('dashboard.html')


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

@myapp_obj.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html')

HOST_NAME = "localhost"
HOST_PORT = 80
DBFILE = "app.db"
app = Flask(__name__)
                                                            # app.debug = True
 
                                                                        #HELPER FUNCTION - SEARCH USERS
def getusers(search):
  conn = sqlite3.connect(DBFILE)
  cursor = conn.cursor()
  cursor.execute(
    "SELECT * FROM `users` WHERE `name` LIKE ? OR `email` LIKE ?",
    ("%"+search+"%", "%"+search+"%",)
  )
  results = cursor.fetchall()
  conn.close()
  return results

@myapp_obj.route("/", methods=["GET", "POST"])
def index():
                                                                                    #SEARCH FOR USERS
  if request.method == "POST":
    data = dict(request.form)
    users = getusers(data["search"])
  else:
    users = []
 
                                                                                    #RENDER HTML PAGE
  return render_template("S3_users.html", usr=users)
 

if __name__ == "__main__":
  app.run(HOST_NAME, HOST_PORT)
