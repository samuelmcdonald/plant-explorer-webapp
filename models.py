from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    favorites = db.relationship('Favorite', back_populates='user')

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plant_name = db.Column(db.String(255), nullable=False)
    plant_common_name = db.Column(db.String(255), nullable=True)
    plant_scientific_name = db.Column(db.String(255), nullable=True)
    plant_image_url = db.Column(db.String(255), nullable=True)
    plant_description = db.Column(db.Text, nullable=True)
    duration = db.Column(db.String(255), nullable=True)
    edible = db.Column(db.Boolean, default=False)
    vegetable = db.Column(db.Boolean, default=False)
    edible_parts = db.Column(db.String(255), nullable=True)
    synonyms = db.Column(db.Text, nullable=True)
    # Add other fields as necessary

    user = db.relationship('User', back_populates='favorites')




    def __repr__(self):
        return '<Favorite {}>'.format(self.plant_name)