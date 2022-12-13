from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
<<<<<<< HEAD
from sqlalchemy.sql import func
=======
from datetime import datetime
>>>>>>> 99e062b783504f932acaad8708329281f25d3843
from app import login
from flask_login import UserMixin
#to create the followers table based on the follower's ID and user's ID
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model, UserMixin):                                                # User class model
    id = db.Column(db.Integer, primary_key = True)                              # User ID
    username = db.Column(db.String, unique=True)                                # Username
    password = db.Column(db.String(200))                                        # password         
    posts = db.relationship('Post', backref='author', lazy='dynamic')           # establishing relationship between user and their posts

<<<<<<< HEAD
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String(200))
    email = db.Column(db.String(32), unique=True)
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
=======
    def set_password(self, password):                                           # set password function
>>>>>>> 99e062b783504f932acaad8708329281f25d3843

        self.password = generate_password_hash(password)

    def check_password(self, password):                                         # check password function
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def remove(self):                                                           # remove/delete account function
        db.session.delete(self)
<<<<<<< HEAD
        
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)

    def get_comments(self):
        return Comment.query.filter_by(post_id=self.id).order_by(Comment.timestamp.desc())

    def __repr__(self):
        return "<Post {}>".format(self.body)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)
=======
    #this function is to let user can follow another user
    def follow(self, user):
        if not self.is_following(user): 
            self.followed.append(user) #this funtion append() is called for the follow function
            return self
     #this function is to let user unfollow the followers
    def unfollow(self, user):
        if self.is_following(user): 
            self.followed.remove(user) #this function remove() is called for the unfollow function
            return self 
    #the user contains two elements: followed and followers. Therefore they can check if they follow each other or not
    def is_following(self, user): #this is to check if a link of two users currently follow each other or not
        return self.followed.filter(
            self.followers.c.followed_id == user.id).count() > 0 #count function is to return number of results

    def followed_posts(self):
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())

    def __repr__(self):
        return '<User %r>' % (self.username)

@login.user_loader
def load_user(id):                                                             # return current user id
    return User.query.get(int(id))

class Post(db.Model):                                                           # post class model
    id = db.Column(db.Integer, primary_key=True)                                # post ID
    body = db.Column(db.String(140))                                            # main text for the post
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)     # post timestamp
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))                   # user ID that submitted the post
    image = db.Column(db.String(20), nullable=True)                             # image file name

    def __repr__(self):
        return "<Post {}>".format(self.body)
>>>>>>> 99e062b783504f932acaad8708329281f25d3843
