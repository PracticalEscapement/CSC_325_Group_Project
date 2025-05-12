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
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)  # Optional field for community image
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
    posts_has_tags = db.relationship('PostHasTag', backref='post_associations', overlaps="tags")

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
    posts = db.relationship('Post', secondary='post_has_tag', backref='tags', overlaps="post_tag_links")

class PostHasTag(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    tag_name = db.Column(db.String(100), db.ForeignKey('tag.name'), primary_key=True)
    post = db.relationship('Post', backref='post_tag_links', overlaps="posts_has_tags")
    tag = db.relationship('Tag', backref='tag_posts')
#Methods data still needs to be implemented

def get_user(user_id):
    users=User.query.filter_by(id=user_id).all()
    data_list=[]
    for user in users:
        data={
            "id": user.id,
            "email": user.email,
            "username":user.username, 
            "communities": user.communities,
            "posts":user.posts,
            "comments":user.comments,
            "notifications":user.notifications,
            "sent_messages":user.sent_messages,
            "recieved_messages":user.received_messages
        }
        data_list.append(data)
    return jsonify(data_list)
def get_community_posts(com_name):
    Com_posts = Post.query.filter_by(com_name=com_name).all()
    post_list = []
    for post in Com_posts:
        post_data = {
            'id': post.id,
            'author_id': post.author_id,
            'com_name': post.com_name,
            'title': post.title,
            'content': post.content,
            'created_at':post.created_at,
            'comments':post.comments,
            'likes':post.like,
            'has_tags': post.posts_has_tags
        }
        post_list.append(post_data)
    return jsonify(post_list)

def get_posts(Post_id):
    Com_posts = Post.query.filter_by(id=Post_id).all()
    post_list = []
    for post in Com_posts:
        post_data = {
            'id': post.id,
            'author_id': post.author_id,
            'com_name': post.com_name,
            'title': post.title,
            'content': post.content,
            'created_at':post.created_at,
            'comments':post.comments,
            'likes':post.like,
            'has_tags': post.posts_has_tags
        }
        post_list.append(post_data)
    return jsonify(post_list)

def get_notifications(user_id):
    Notifs=Notification.query.filter_by(belongs_to_user_id=user_id).all()
    data_list=[]
    for notifications in Notifs:
        data={
            "id":notifications.id,
            "Belongs_to_id": notifications.belongs_to_user_id,
            "is_read":notifications.is_read,
            "created_at":notifications.created_at,
            "message":notifications.message,
            "link":notifications.link


        }
        data_list.append(data)
    return jsonify(data_list)

def get_all_users():
    users=User.query.all()
    data_list=[]
    for user in users:
        data={

            "username":user.username, 
            "id": user.id,
            "email": user.email,
            "communities": user.communities,
            "posts":user.posts,
            "comments":user.comments,
            "notifications":user.notifications,
            "sent_messages":user.sent_messages,
            "recieved_messages":user.received_messages
        }
        data_list.append(data)
    return jsonify(data_list)

def get_messages(receiver_id):
    mes=Message.query.filter_by(receiver_id=receiver_id).all()
    data_list=[]
    for messages in mes:
        data={
            "id":messages.id,
            "sender_id": messages.sender_id,
            "reciever_id":messages.receiver_id,
            "content":messages.content,
            "created_at": messages.created_at,
            "is_read":messages.is_read
        }
        data_list.append(data)
    return jsonify(data_list)

def get_comments(post_id):
    com=Comment.query.filter_by(post_id=post_id).all()
    data_list=[]
    for comments in com:
        data={
            "id": comments.id,
            "author":comments.author_id,
            "created_date":comments.created_at,
            "content":comments.content,
            "likes_id":comments.like.id
        } 
        data_list.append(data)
    return jsonify(data_list)

def get_all_comminities():
    community=Community.query.all()
    data_list=[]
    for communities in community:
        data={
            "name":communities.name,
            "author_id":communities.author_id,
            "created_at":communities.created_at,
            "num_memebers":communities.num_memebers,
            "Description":communities.description,
            "img_url":communities.img_url,
            "author":communities.author,
            "posts":communities.posts,
        }
        data_list.append(data)
    return jsonify(data_list)
def get_user_community(user_id):
    # Query the Member table to get all memberships for the user
    memberships = Member.query.filter_by(member_id=user_id).all()
    data_list = []

    print("Memberships:", memberships)
    for membership in memberships:
        # Use the community_name from the Member table to fetch the Community
        community = Community.query.filter_by(name=membership.community_name).first()
        if community:
            data = {
                "name": community.name,
                "description": community.description,
                "image_url": community.image_url,
                "author_id": community.author_id,
                "created_at": community.created_at,
                "num_members": community.num_members,
                "author": community.author.username,  # Assuming you want the author's username
                "posts": [post.title for post in community.posts],  # Example: list of post titles
            }
            data_list.append(data)

    return jsonify(data_list)

def get_community(name):
    community=Community.query.filter_by(name=name).all()
    data_list=[]

    data={
        "name":community.name,
        "author_id":community.author_id,
        "created_at":community.created_at,
        "num_memebers":community.num_memebers,
        "Description":community.description,
        "img_url":community.img_url,
        "author":community.author,
        "posts":community.posts,
    }
    data_list.append(data)
    return jsonify(data_list)

def is_user_member_of_community(user_id, community_name):
    """
    Check if a user is a member of a specific community.
    """
    membership = Member.query.filter_by(member_id=user_id, community_name=community_name).first()
    return membership is not None

def get_memebers(community_name):
    members=Member.query.filter_by(name=community_name).all()
    data_list=[]
    for membr in members:
        data={
            "member": membr.member_id,
            "community":membr.community_name
            
        }
        data_list.append(data)
    return jsonify(data_list)

def get_user_posts(user_id):
    Numpost = Post.query.filter_by(author_id=user_id).all()
    post_list = []
    for post in Numpost:
        post_data = {
            'id': post.id,
            'author_id': post.author_id,
            'com_name': post.com_name,
            'title': post.title,
            'content': post.content,
            'created_at':post.created_at,
            'comments':post.comments,
            'likes':post.like,
            'has_tags': post.posts_has_tags
        }
        post_list.append(post_data)
    return jsonify(post_list)


