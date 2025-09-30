from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, InputRequired


class RegForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email(message="Invalid email")])
    password = PasswordField("Password", validators=[InputRequired()])
    name = StringField("Name")
