from . import db
from flask_login import UserMixin
from flask import jsonify
from sqlalchemy.sql import func

#---User-related:
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False) 
    email= db.Column(db.String(150), unique=True, nullable=False)
    username= db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    communities = db.relationship('Member')
    posts = db.relationship('Post')
    comments = db.relationship('Comment')
    likes = db.relationship('Like')
    notifications = db.relationship('Notification')
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender')
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver_user')

    def __repr__(self):
        return f'<User {self.username}>'
    
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    belongs_to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_read = db.Column(db.Boolean, nullable=False)
    #TODO: needs to be finished
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    message = db.Column(db.String(300), nullable=False)  # e.g., "You got a new like on your post"
    link = db.Column(db.String(300))  # optional, like '/post/5'

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    is_read = db.Column(db.Boolean, nullable=False)

#---Community-related
class Community(db.Model):
    name = db.Column(db.String(200), primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    num_members = db.Column(db.Integer)
    members = db.relationship('Member')
    posts = db.relationship('Post')
    author = db.relationship('User', backref='owns_communities')

class Member(db.Model):
    member_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    community_name = db.Column(db.String(200), db.ForeignKey('community.name'), primary_key=True)

#---Post-related
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    com_name = db.Column(db.String(200), db.ForeignKey('community.name'), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.String(20000), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    comments = db.relationship('Comment', backref='post', cascade="all, delete")
    likes = db.relationship('Like', backref='post', cascade="all, delete")
    posts_has_tags = db.relationship('PostHasTag')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    content = db.Column(db.String(400), nullable=False)
    likes = db.relationship('Like', backref='comment')

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    liked_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    belongs_to_post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
    belongs_to_comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)

#---Tags
class Tag(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    posts = db.relationship('Post', secondary='post_has_tag', backref='tags')

class PostHasTag(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    tag_name = db.Column(db.String(100), db.ForeignKey('tag.name'), primary_key=True)
    post = db.relationship('Post', backref='post_tags')
    tag = db.relationship('Tag', backref='tag_posts')
#Methods data still needs to be implemented
def get_notifications(user_id):
    Notifs=Notification.query.filter_by(belongs_to_user_id=user_id).all()
    data_list=[]
    for user in users:
        data={
            "id": user.belongs_to_user_id

        }
        data_list.append(data)
    return jsonify(data_list)

def get_all_users():
    users=User.query.all()
    data_list=[]
    for user in users:
        data={
            "id": user.id,
            "email": user.email
        }
        data_list.append(data)
    return data_list
def get_messages(receiver_id):
    mes=Message.query.filter_by(receiver_id=receiver_id).all()
    data_list=[]
    for user in users:
        data={
            "id": user.id
        }
        data_list.append(data)
    return jsonify(data_list)
def get_comments(post_id):
    com=Comment.query.filter_by(post_id=post_id).all()
    data_list=[]
    for user in users:
        data={
            "id": user.id
        }
        data_list.append(data)
    return jsonify(data_list)

def get_memebers(community_name):
    commun=Community.query.filter_by(community_name=community_name).all()
    data_list=[]
    for user in users:
        data={
            "member": member_id
        }
        data_list.append(data)
    return jsonify(data_list)
def get_all_posts(user_id):
    Numpost = Post.query.filter_by(author_id=user_id).all()
    post_list = []
    for post in Numpost:
        post_data = {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author_id': post.author_id,
            'author_username': post.author.username,  
            'com_name': post.com_name,
            'created_at': post.created_at
        }
        post_list.append(post_data)
    return jsonify(post_list)


