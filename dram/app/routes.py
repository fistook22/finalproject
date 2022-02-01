from flask import redirect, render_template, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, db, models
from app.models import User, Whisky
from app.forms import LoginForm, RegisterForm, Taste
from flask_login import login_user, login_required, logout_user, current_user


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('history'))

        return '<h1>Invalid username or password</h1>'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                        country=form.country.data, gender=form.gender.data)
        db.session.add(new_user)
        db.session.commit()

        return f'<h1>Hey {new_user}! lets taste some whisky!</h1>'

    return render_template('signup.html', form=form)


@app.route('/history')
@login_required
def history():
    return render_template('history.html', user=User.query.filter_by(id=current_user.get_id()).first())


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/taste', methods=['GET', 'POST'])
@login_required
def taste():
    form = Taste()
    user = User.query.filter_by(id=current_user.get_id())

    def get_country():
        for column in user:
            return user.country

    user_country = get_country()

    def get_gender():
        for column in user:
            return user.gender

    user_gender = get_gender()

    if form.validate_on_submit():
        new_whisky = Whisky(distillery=form.distillery.data, edition=form.edition.data, color=form.color.data,
                            smokey=form.smokey.data, peaty=form.peaty.data, spicy=form.spicy.data,
                            sweet=form.sweet.data,
                            fresh_fruit=form.fresh_fruit.data, dried_fruit=form.dried_fruit.data,
                            red_fruit=form.red_fruit.data,
                            feinty=form.feinty.data, floral=form.floral.data, winey=form.winey.data, oak=form.oak.data,
                            cereal=form.cereal.data, chocolate=form.chocolate.data, finish=form.finish.data,
                            description=form.description.data, user_id=current_user.get_id(),
                            user_country=user_country, user_gender=user_gender)
        db.session.add(new_whisky)
        db.session.commit()

        return f'<h1>{new_whisky.distillery} {new_whisky.edition} was added to the DB</h1>'

    return render_template('taste.html', form=form)
