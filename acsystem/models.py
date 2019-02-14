from acsystem import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    first = db.Column(db.String(60), nullable=False)
    last = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), unique= True, nullable=False)
    image_file = db.Column(db.String(20), default='default.jpg', nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    companies = db.relationship('Company', backref ='owner', lazy = True, cascade="all, delete-orphan")
    activecompany = db.Column(db.Integer)
    
    def __init__(self, first, last, email, phone, password):
        self.first = first
        self.last = last
        self.email = email
        self.phone = phone
        self.password = password

    def __repr__(self):
        return f"User('{self.first} {self.activecompany}' )"


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyname = db.Column(db.String(80), unique=True, nullable=False)
    mailingname = db.Column(db.String(80), nullable = False)
    address = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(40), nullable=False)
    state = db.Column(db.String(40), nullable=False)
    pin = db.Column(db.Integer)
    email = db.Column(db.String(60))
    phoneno = db.Column(db.Integer)
    website = db.Column(db.String(60))
    datecreated = db.Column(db.DateTime, default = datetime.utcnow, nullable=False)
    gstno = db.Column(db.Integer)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f"Company('{self.companyname}', '{self.owner.first}')"


class Countries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    states = db.relationship('States', backref='countries', lazy=True)

class States(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    country = db.Column(db.Integer, db.ForeignKey('countries.id'))
