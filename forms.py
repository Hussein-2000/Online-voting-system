from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class admin_login_form(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password =  PasswordField('Password', validators=[DataRequired()])
    Login = SubmitField('Login')


class User_login_form(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password =  PasswordField('Password', validators=[DataRequired()])
    Login = SubmitField('Login')