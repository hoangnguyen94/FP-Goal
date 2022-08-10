from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length


class CreateUserForm(FlaskForm):
    """form to create a users."""

    username = StringField('Username', 
        validators=[DataRequired()])
    password = PasswordField('Password', 
        validators=[DataRequired(), Length(min=6)])
    email = StringField('E-mail',
        validators=[DataRequired(), Email()])
    firstname = StringField('First Name',
        validators=[DataRequired()])
    lastname = StringField('Last Name',
        validators=[DataRequired()])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', 
        validators=[DataRequired()])
    password = PasswordField('Password', 
        validators=[Length(min=6)])

class AddClientForm(FlaskForm):
    """form to add clients to user"""

    name = StringField('Full Name',
        validators=[DataRequired()])
    email = StringField('E-mail',
        validators=[DataRequired(),Email()])
    gender = SelectField('Gender', 
        choices=[('M', 'Male'), ('F', 'Female')])
    age = IntegerField('Age', 
        validators=[DataRequired()])

class FoodSearchForm(FlaskForm):
    "form to search for food."

    food = StringField('Food',
        validators=[DataRequired])
    quantity = IntegerField('Quantity',
        validators=[DataRequired()])