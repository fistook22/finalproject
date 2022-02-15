import os

import matplotlib.pyplot as plt
from flask import redirect, render_template, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from app import app, db, ALLOWED_EXTENSIONS
from app.forms import LoginForm, RegisterForm, Taste
from app.models import User, Whisky


@app.route('/')
def index():
    whisky_data = Whisky.query.all()
    return render_template('index.html', whisky_data=whisky_data)


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

        return redirect(url_for('index'))

    return render_template('signup.html', form=form)


@app.route('/history')
@login_required
def history():
    return render_template('history.html', user_whisky_history=Whisky.query.filter_by(user_id=current_user.get_id()))


@app.route('/whisky/<whisky_id>', methods=['GET', 'POST'])
@login_required
def whisky(whisky_id):
    whisky_page = Whisky.query.filter_by(id=whisky_id).first()
    return render_template('whisky.html', whisky=whisky_page)


@app.route('/delete/<whisky_id>', methods=['GET', 'POST'])
@login_required
def delete(whisky_id):
    whisky_delete = Whisky.query.filter_by(id=whisky_id).first()

    try:
        db.session.delete(whisky_delete)
        db.session.commit()
        return redirect(url_for('history'))
    except:
        return "failed to delete"


@app.route('/update/<whisky_id>', methods=['GET', 'POST'])
@login_required
def update(whisky_id):
    whisky_delete = Whisky.query.filter_by(id=whisky_id).first()
    db.session.delete(whisky_delete)
    db.session.commit()
    return redirect(url_for('taste'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/taste', methods=['GET', 'POST'])
@login_required
def taste():
    form = Taste()
    user = User.query.filter_by(id=current_user.get_id())
    whisky_count = Whisky.query.count()

    def get_country():
        for column in user:
            return column.country

    user_country = get_country()

    def get_gender():
        for column in user:
            return column.gender

    user_gender = get_gender()

    if form.validate_on_submit():
        i = form.image.data
        image = secure_filename(i.filename)
        i.save(os.path.join(app.config['UPLOAD_FOLDER'], image))

        size_label = {'smokey': form.smokey.data, 'peaty': form.peaty.data, 'spicy': form.spicy.data,
                      'sweet': form.sweet.data, 'fresh_fruit': form.fresh_fruit.data,
                      'dried_fruit': form.dried_fruit.data,
                      'red_fruit': form.red_fruit.data, 'feinty': form.feinty.data, 'floral': form.floral.data,
                      'winey': form.winey.data,
                      'oak': form.oak.data, 'cereal': form.cereal.data, 'chocolate': form.chocolate.data}

        size_label_without_zero = {k: v for k, v in size_label.items() if v > 0}
        labels = list(size_label_without_zero.keys())
        sizes = list(size_label_without_zero.values())

        fig1, ax1 = plt.subplots()

        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                startangle=90, labeldistance=1.1)

        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.savefig('app/static/whisky_images/' + 'whisky_plot' + str(Whisky.query.count() + 1) + '.jpg')  # .show()

        new_whisky = Whisky(distillery=form.distillery.data, edition=form.edition.data, color=form.color.data,
                            smokey=form.smokey.data, peaty=form.peaty.data, spicy=form.spicy.data,
                            sweet=form.sweet.data,
                            fresh_fruit=form.fresh_fruit.data, dried_fruit=form.dried_fruit.data,
                            red_fruit=form.red_fruit.data,
                            feinty=form.feinty.data, floral=form.floral.data, winey=form.winey.data, oak=form.oak.data,
                            cereal=form.cereal.data, chocolate=form.chocolate.data, finish=form.finish.data,
                            image=i.filename, plot='whisky_plot' + str(Whisky.query.count() + 1) + '.jpg',
                            description=form.description.data, user_id=current_user.get_id(),
                            user_country=user_country, user_gender=user_gender)
        db.session.add(new_whisky)
        db.session.commit()

        return redirect(url_for('history'))

    return render_template('taste.html', form=form, whisky=whisky)

# def get_smokey():
#     for column in whisky:
#         return column.smokey
#
# smokey_taste = get_smokey()
#
# def get_peaty():
#     for column in whisky:
#         return column.peaty
#
# peaty_taste = get_peaty()
#
# def get_spicy():
#     for column in whisky:
#         return column.spicy
#
# spicy_taste = get_spicy()
#
# def get_sweet():
#     for column in whisky:
#         return column.sweet
#
# sweet_taste = get_sweet()
#
# def get_fresh_fruit():
#     for column in whisky:
#         return column.fresh_fruit
#
# fresh_fruit_taste = get_fresh_fruit()
#
# def get_dried_fruit():
#     for column in whisky:
#         return column.dried_fruit
#
# dried_fruit_taste = get_dried_fruit()
#
# def get_red_fruit():
#     for column in whisky:
#         return column.red_fruit
#
# red_fruit_taste = get_red_fruit()
#
# def get_feinty():
#     for column in whisky:
#         return column.feinty
#
# feinty_taste = get_feinty()
#
# def get_floral():
#     for column in whisky:
#         return column.floral
#
# floral_taste = get_floral()
#
# def get_winey():
#     for column in whisky:
#         return column.winey
#
# winey_taste = get_winey()
#
# def get_oak():
#     for column in whisky:
#         return column.oak
#
# oak_taste = get_oak()
#
# def get_cereal():
#     for column in whisky:
#         return column.cereal
#
# cereal_taste = get_cereal()
#
# def get_chocolate():
#     for column in whisky:
#         return column.chocolate
#
# chocolate_taste = get_chocolate()
# labels = 'smokey', 'peaty', 'spicy', 'sweet', 'fresh_fruit', 'dried_fruit', 'red_fruit', 'feinty', 'floral', 'winey', 'oak', 'cereal', 'chocolate'
# sizes = [form.smokey.data, form.peaty.data, form.spicy.data, form.sweet.data, form.fresh_fruit.data,
#          form.dried_fruit.data,
#          form.red_fruit.data,
#          form.feinty.data, form.floral.data, form.winey.data, form.oak.data, form.cereal.data,
#          form.chocolate.data]
# for size in size_label:
#     if size_label.values() == 0:
#         del size_label[size]
