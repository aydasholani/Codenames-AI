from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.String(6), primary_key=True, unique=True, nullable=False)
    owner_id = db.Column(db.Integer(), nullable=False)
    
    users = db.relationship('User', backref='room', lazy=True, cascade="all, delete")
    team = db.relationship('Team', backref='room', lazy=True, cascade="all, delete")
    
    def to_dict(self):
        return {
            'id': self.id,
            'id': self.id,
            'owner_id': self.owner_id,
            'users': [user.to_dict() for user in self.users],
            'teams': [team.to_dict() for team in self.team]
        }

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer(), primary_key=True)
    color = db.Column(db.String(10), nullable=False)  # Lagets färg
    room_id = db.Column(db.String(6), db.ForeignKey('rooms.id'), nullable=False)
    
    users = db.relationship('User', backref='team', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'color': self.color,
            'users': [user.to_dict() for user in self.users],
            'room_id': self.room_id
        }

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    session_id = db.Column(db.String(100), nullable=False)
    is_agent = db.Column(db.Boolean(), default=False)
    room_id = db.Column(db.String(6), db.ForeignKey('rooms.id'), nullable=False)
    team_id = db.Column(db.Integer(), db.ForeignKey('teams.id'), nullable=True)
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'session_id': self.session_id,
            'is_agent': self.is_agent,
            'room_id': self.room_id,
            'team_id': self.team_id
        }

    def __init__(self, username, room_id, session_id):
        self.username = username
        self.room_id = room_id
        self.session_id = session_id
