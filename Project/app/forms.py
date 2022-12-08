from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired,Email,EqualTo,InputRequired,Length,ValidationError

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    
    remember_me = BooleanField('Remember me')

    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')
    
    def validate_username(self, username):                      #if user enters already existing username to signup
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

class PostForm(FlaskForm):
    post = TextAreaField('Post Something', validators=[
        DataRequired(), Length(min=1, max=280)])
    image = FileField('Add image to your post', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')