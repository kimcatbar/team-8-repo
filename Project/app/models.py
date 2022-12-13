from app import myapp_obj, db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import login
from flask_login import UserMixin
import os
from datetime import datetime
from sqlalchemy.sql import func
from . import db




#to create the followers table based on the follower's ID and user's ID
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String(200))
    email = db.Column(db.String(32), unique=True)
    followed = db.relationship('User',  #this is to link user to another user's account. This is a parent class
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),   #this is to link to the table with the condition is the follower's ID
        secondaryjoin=(followers.c.followed_id == id), #to configured the table with the condition is the follow's ID
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic') #to define the relationship start at follower to mode dynamic
    #to let user can follower another users 
    #it will presendted under the table which user an see who user currently follow
    #this is to show that message is sent by the user
    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    #this is to show the message is received by followed
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def remove(self):
        db.session.delete(self)
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
    #this is to check who are followed by users
    
    def showfollowing(self, user): 
        return self.followed.filter(
            self.followers.c.following_id == user.id).count() > 0 #count function is to return number of results      
    
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())
    
class Post(db.Model):                                                           # post class model
    id = db.Column(db.Integer, primary_key=True)                                # post ID
    body = db.Column(db.String(140))                                            # main text for the post
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)     # post timestamp
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))                   # user ID that submitted the post
                       

    def __repr__(self):
        return "<Post {}>".format(self.body)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#this is to extend for the user can send private message to the followed 
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id')) #this is for the sender 
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id')) #this is for the receiver
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow) #this shows the time when user read the message

    def __repr__(self):
        return '<Message {}>'.format(self.body)

