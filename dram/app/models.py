from flask_login import UserMixin, current_user

from app import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(120))
    country = db.Column(db.String(64))
    gender = db.Column(db.String(2))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Whisky(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    distillery = db.Column(db.String(64))
    edition = db.Column(db.String(64))

    color = db.Column(db.String(64))

    smokey = db.Column(db.Integer)
    peaty = db.Column(db.Integer)
    spicy = db.Column(db.Integer)
    sweet = db.Column(db.Integer)
    fresh_fruit = db.Column(db.Integer)
    dried_fruit = db.Column(db.Integer)
    red_fruit = db.Column(db.Integer)
    feinty = db.Column(db.Integer)
    floral = db.Column(db.Integer)
    winey = db.Column(db.Integer)
    oak = db.Column(db.Integer)
    cereal = db.Column(db.Integer)
    chocolate = db.Column(db.Integer)
    finish = db.Column(db.String(32))
    image = db.Column(db.String(120))
    plot = db.Column(db.String(120))
    description = db.Column(db.String(120))

    user_id = db.Column(db.Integer)
    user_country = db.Column(db.String(32))
    user_gender = db.Column(db.String(32))

