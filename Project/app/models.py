from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import login
from flask_login import UserMixin


class User(db.Model, UserMixin):                                                # User class model
    id = db.Column(db.Integer, primary_key = True)                              # User ID
    username = db.Column(db.String, unique=True)                                # Username
    password = db.Column(db.String(200))                                        # password         
    posts = db.relationship('Post', backref='author', lazy='dynamic')           # establishing relationship between user and their posts
    comments = db.relationship('Comment', backref='user', passive_deletes=True)

    def set_password(self, password):                                           # set password function
        self.password = generate_password_hash(password)

    def check_password(self, password):                                         # check password function
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def remove(self):                                                           # remove/delete account function
        db.session.delete(self)

    def my_posts(self):
        own = Post.query.filter_by(user_id=self.id)
        return own.order_by(Post.timestamp.desc())

@login.user_loader
def load_user(id):                                                             # return current user id
    return User.query.get(int(id))

class Post(db.Model):                                                           # post class model
    id = db.Column(db.Integer, primary_key=True)                                # post ID
    body = db.Column(db.String(140))                                            # main text for the post
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)     # post timestamp
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))                   # user ID that submitted the post
    image = db.Column(db.String(20), nullable=True)                             # image file name
    comments = db.relationship('Comment', backref='post', passive_deletes=True)

    def __repr__(self):
        return "<Post {}>".format(self.body)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)