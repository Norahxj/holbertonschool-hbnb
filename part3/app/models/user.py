import re
from sqlalchemy.orm import validates
from app.extensions import db, bcrypt
from app.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    places = db.relationship('Place', backref='owner', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.password = None
        self.hash_password(password)

    @validates('first_name')
    def validate_first_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError("first_name is required and must be <= 50 characters")
        return value

    @validates('last_name')
    def validate_last_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError("last_name is required and must be <= 50 characters")
        return value

    @validates('email')
    def validate_email(self, key, value):
        pattern = r"^[^@]+@[^@]+\.[^@]+$"
        if not re.match(pattern, value):
            raise ValueError("Invalid email format")
        return value

    def hash_password(self, password):
        if not password:
            raise ValueError("Password is required")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        })
        return data
