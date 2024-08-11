from datetime import datetime
from applications.database import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security,UserMixin, RoleMixin



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(100), nullable=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    fs_token_uniquifier = db.Column(db.String(255), unique=True)
    active = db.Column(db.Boolean())

    # Relationships
    roles = db.relationship('Role', secondary='role_user', backref=db.backref('users', lazy=True))
    borrowed_books = db.relationship('BorrowedBooks', backref='borrower', lazy=True)
    all_activity = db.relationship('AllActivity', backref='actor', lazy=True)
    requests = db.relationship('Request', backref='requester', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Role(db.Model, RoleMixin):
    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30),nullable=False)
    description = db.Column(db.String(100),nullable=True)

    def __repr__(self):
        return f'<Role {self.name}>'

class RoleUser(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30),db.ForeignKey('user.username'))
    role_id = db.Column(db.Integer,db.ForeignKey('role.role_id'))

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow,nullable=True)

    # Relationships
    books = db.relationship('Book', backref='section', lazy=True)
    

    def __repr__(self):
        return f'<Section {self.section_name}>'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    authors = db.Column(db.String(255), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    date_created= db.Column(db.DateTime, default=datetime.utcnow,nullable=True)

    # Relationships
    requests = db.relationship('Request', backref='book', lazy=True)
    borrowed_books = db.relationship('BorrowedBooks', backref='user', lazy=True)
    activity_logs = db.relationship('AllActivity', backref='user', lazy=True)

    def __repr__(self):
        return f'<Book {self.name}>'

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    date_of_request = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Request {self.id} - {self.status}>'

class BorrowedBooks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<BorrowedBooks {self.id} - {self.status}>'


class AllActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    requested_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    approved_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<AllActivity {self.id} - {self.status}>'
    
class UserLogins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    logout_time = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<UserLogins {self.id} - User {self.user_id}>'
