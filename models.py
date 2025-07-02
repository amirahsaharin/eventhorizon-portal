from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'  # ✅ Force lowercase table name

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(20))  # 'organizer' or 'attendee'

class Event(db.Model):
    __tablename__ = 'events'  # ✅ Force lowercase table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date = db.Column(db.String(50))
    location = db.Column(db.String(100))
    capacity = db.Column(db.Integer)
    description = db.Column(db.Text)

class Registration(db.Model):
    __tablename__ = 'registrations'  # ✅ Force lowercase table name

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
