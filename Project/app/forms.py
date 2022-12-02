from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired,Email,EqualTo

class LoginForm(FlaskForm):
    """
    """

class RegistrationForm(FlaskForm):
    """
    """