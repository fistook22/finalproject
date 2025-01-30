from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, IntegerRangeField, SelectField, RadioField, SubmitField, FileField
from wtforms.validators import InputRequired, Length, Email, DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=120)])
    remember = BooleanField('Remember me')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=120)])
    country = StringField('Country', validators=[InputRequired()])
    gender = RadioField('Gender', choices=['M', 'F'])


class Taste(FlaskForm):
    distillery = StringField('Distillery', validators=[DataRequired()])
    edition = StringField('Edition', validators=[DataRequired()])

    color = SelectField('Color',
                        choices=[("Gold", "Gold"), ("Light gold", "Light gold"), ("Deep gold", "Deep gold"),
                                 ("Amber", "Amber"), ("Mahogany", "Mahogany"), ("Brown sherry", "Brown sherry")]
                        , default=None)

    smokey = IntegerRangeField('Smokey', default=None)
    peaty = IntegerRangeField('Peaty', default=None)
    spicy = IntegerRangeField('Spicy', default=None)
    sweet = IntegerRangeField('Sweet', default=None)
    fresh_fruit = IntegerRangeField('Fresh_fruit', default=None)
    dried_fruit = IntegerRangeField('Dried_fruit', default=None)
    red_fruit = IntegerRangeField('Red_fruit', default=None)
    feinty = IntegerRangeField('Feinty', default=None)
    floral = IntegerRangeField('Floral', default=None)
    winey = IntegerRangeField('Winey', default=None)
    oak = IntegerRangeField('Oak', default=None)
    cereal = IntegerRangeField('Cereal', default=None)
    chocolate = IntegerRangeField('Chocolate', default=None)

    finish = SelectField('Finish',
                         choices=[("Very short", "Very short"), ("Short", "Short"), ("Medium", "Medium"),
                                  ("Long", "Long"), ("Very long", "Very long")]
                         , default=None)

    image = FileField('image', validators=[DataRequired()])
    description = StringField('description')

    submit = SubmitField('Add to My Whisky List')
