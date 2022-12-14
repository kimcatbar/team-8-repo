from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired,InputRequired,Length,ValidationError
from flask_babel import lazy_gettext

class LoginForm(FlaskForm):                                                 # log in form with username, password, remember me, and submit fields

    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": lazy_gettext("Username") })

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": lazy_gettext("Password") })
    
    remember_me = BooleanField(lazy_gettext('Remember me'))

    submit = SubmitField(lazy_gettext('Login'))

class RegistrationForm(FlaskForm):                                         # registration form with username, password, and submit fields
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": lazy_gettext("Username") })

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": lazy_gettext("Password")})

    submit = SubmitField(lazy_gettext('Register'))
    
    def validate_username(self, username):                      #if user enters already existing username to signup
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                lazy_gettext('That username already exists. Please choose a different one.'))

class PostForm(FlaskForm):                                              # post form with post body, image, and submit fields
    post = TextAreaField(lazy_gettext('Post Something'), validators=[
        DataRequired(), Length(min=1, max=280)])
    image = FileField(lazy_gettext('Add image to your post'), validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField(lazy_gettext('Submit'))

class EmptyForm(FlaskForm):                                             # submit form for follow and unfollow   
    submit = SubmitField(lazy_gettext('Submit'))