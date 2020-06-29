from capstone import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('BlogPost',backref='author',lazy=True,order_by='BlogPost.date')

    def __init__(self,email,password):
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Username {self.username}"


class BlogPost(db.Model):

    users = db.relationship(User)

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    file = db.Column(db.String(64),nullable=False,default='default.txt')
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    title = db.Column(db.String(140),nullable=False)
    
    def __init__(self,title,user_id,file):
        self.title = title
        self.user_id = user_id
        self.file=file

    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date} --- {self.title}"


class ContactPost(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text,nullable=False)
    number = db.Column(db.String(20), nullable=False)
    def __init__(self,name,email,number,message):
        self.name = name
        self.email = email
        self.number=number
        self.message=message

    def __repr__(self):
        return f"Post ID: {self.id} -- Name: {self.name}"





