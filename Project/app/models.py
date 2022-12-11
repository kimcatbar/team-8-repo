from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from app import login
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String(200))
    email = db.Column(db.String(32), unique=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def remove(self):
        db.session.delete(self)
        
    def my_posts(self):
        own = Post.query.filter_by(user_id=self.id)
        return own.order_by(Post.timestamp.desc())
    
    def blog_posts(self):
        return Post.query.order_by(Post.timestamp.desc())

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):#class Post creates a user text post 
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='title', lazy='dynamic')

    def get_comments(self):
        return Comment.query.filter_by(post_id=self.id).order_by(Comment.timestamp.desc())

    def __repr__(self):
        return "<Post {}>".format(self.body)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)