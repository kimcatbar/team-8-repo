from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
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
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    followed = db.relationship('User',  #this is to link user to another user's account. This is a parent class
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),   #this is to link to the table with the condition is the follower's ID
        secondaryjoin=(followers.c.followed_id == id), #to configured the table with the condition is the follow's ID
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic') #to define the relationship start at follower to mode dynamic
    #to let user can follower another users 
    #it will presendted under the table which user an see who user currently follow

    def set_password(self, password):                                           # set password function

        self.password = generate_password_hash(password)

    def check_password(self, password):                                         # check password function
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def remove(self):                                                           # remove/delete account function
        db.session.delete(self)
    #this function is to let user can follow another user

    def __repr__(self):
        return '<User %r>' % (self.username)

    def follow(self, user):
        if not self.is_following(user): 
            self.followed.append(user) #this funtion append() is called for the follow function
     #this function is to let user unfollow the followers
    def unfollow(self, user):
        if self.is_following(user): 
            self.followed.remove(user) #this function remove() is called for the unfollow function
    #this is to check who are followed by users
    
    def is_following(self, user): 
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0 #count function is to return number of results      
    
    def followed_posts(self):
        return Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id).order_by(
                    Post.timestamp.desc()
                )
        

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

class Comment(db.Model):                                                        # Comment class with id, text body, timestamp, user ID, and the post ID
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)
