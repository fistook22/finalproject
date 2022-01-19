from flask_login import UserMixin

from app import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(120))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



