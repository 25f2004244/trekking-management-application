from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class user(db.Model):
    user_id = db.Column(db.Integer , primary_key = True , autoincrement = True)
    username = db.Column(db.String(50),nullable=False)
    role=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(50),unique=True,nullable=False)
    password=db.Column(db.String(20),nullable=False)

    bookings = db.relationship('booking', backref='user')

    def __repr__(self):
        return '<user (email=%s, username=%s)>' %(self.email,self.username)


class staff(db.Model):
    staff_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    staff_name = db.Column(db.String(50),nullable=False)

    treks = db.relationship('trek', backref='staff')




class trek(db.Model):
    trek_id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    name = db.Column(db.String(50),nullable=False)
    difficulty = db.Column(db.String(20),nullable=False)
    duration = db.Column(db.Integer,nullable=False)
    slots = db.Column(db.Integer,nullable=False)
    assigned_staff = db.Column(db.Integer,db.ForeignKey(staff.staff_id))
    status = db.Column(db.String(20),nullable=False)

    bookings = db.relationship('booking', backref='trek')




class booking(db.Model):
    booking_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey(user.user_id))
    trek_id = db.Column(db.Integer,db.ForeignKey(trek.trek_id))
    booking_status = db.Column(db.String(20),nullable=False)
    booking_date = db.Column(db.DateTime,default=datetime.now)
    payment_status = db.Column(db.String(20),nullable=False)

