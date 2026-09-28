from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()



class user(db.Model):
    user_id = db.Column(db.Integer , primary_key = True , autoincrement = True)
    username = db.Column(db.String(50),nullable=False)
    role=db.Column(db.String(5),nullable=False)
    email=db.Column(db.String(50),unique=True,nullable=False)
    password=db.Column(db.String(20),nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    bookings = db.relationship('booking', backref='user')





class trek(db.Model):
    trek_id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    name = db.Column(db.String(20),nullable=False)
    difficulty = db.Column(db.String(10),nullable=False)
    duration = db.Column(db.Integer,nullable=False)
    slots = db.Column(db.Integer,nullable=False)
    assigned_staff = db.Column(db.Integer,db.ForeignKey(user.user_id),nullable=True)
    status = db.Column(db.String(10),default='Open')
    location = db.Column(db.String(10200),default='To be announced')

    bookings = db.relationship('booking', backref='trek',cascade="all, delete")
    staff = db.relationship('user', backref='treks_assigned')




class booking(db.Model):
    booking_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey(user.user_id),nullable=False)
    trek_id = db.Column(db.Integer,db.ForeignKey(trek.trek_id),nullable=False)
    booking_status = db.Column(db.String(10),default='pending')
    booking_date = db.Column(db.DateTime,default=datetime.now)

