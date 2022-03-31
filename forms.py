from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Email, Length, Regexp

class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=40), Regexp('^\w+$', message="Must only contain letters numbers or underscore")])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    first_name = StringField("First Name", validators=[InputRequired(), Length(min=1, max=40)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=1, max=40)])

class ClearForm(FlaskForm):
    """"""

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=2, max=55)])

class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(min=2, max=50)])
    content = StringField("Feedback", validators=[InputRequired(), Length(min=2, max=500)])

