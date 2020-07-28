from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Application.models import Users, Posts
from flask_login import current_user

class PostForm(FlaskForm):
    title = StringField("Title",
    validators = [
        DataRequired(),
        Length(min=2, max=100)
    ])
    content = StringField("Content",
    validators = [
        Length(min=2, max=500)
    ])
    submit = SubmitField("Post!")


class RegistrationForm(FlaskForm):
    email = StringField("Email",
    validators = [
        DataRequired(),
        Email()
    ])
    password = PasswordField("Password",
    validators = [
        DataRequired()
    ])
    confirm_password = PasswordField("Confirm your password",
    validators = [
        DataRequired(),
        EqualTo("password")
    ])
    first_name = StringField("First Name",
    validators = [
        DataRequired(),
        Length(min=2, max=30)
    ])
    last_name = StringField("Last Name",
    validators = [
        DataRequired(),
        Length(min=2, max=30)
    ])
    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email is already in use")

class LoginForm(FlaskForm):
    email = StringField("Email",
    validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField("Password", 
    validators=[
        DataRequired()
    ])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class UpdateAccountForm(FlaskForm):
    email = StringField("Email",
    validators = [
        DataRequired(),
        Email()
    ])
    first_name = StringField("First Name",
    validators = [
        DataRequired(),
        Length(min=2, max=30)
    ])
    last_name = StringField("Last Name", 
    validators = [
        DataRequired(),
        Length(min=2, max=30)
    ])
    submit = SubmitField("Edit Account")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email already in use")