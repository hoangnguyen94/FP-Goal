"Models for Nutritiom app"

from codecs import backslashreplace_errors
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User in system"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False,unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)

    clients = db.relationship(
        "Client",
        backref="users")
    
    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, password, email, firstname, lastname):
        """Signup user. Hashes password and adds user to system."""
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        
        user = User(
            username=username,
            password = hashed_pwd,
            email=email,
            firstname=firstname,
            lastname=lastname
        )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.
        
        This is a class method to search for a user with password 
        hash matches this password.
        If can't find matching user returns False."""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Client(db.Model):
    """Client that connect to User"""

    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    user_name_id = db.Column(db.Integer, 
                db.ForeignKey('users.id', ondelete="cascade"))
    email = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    gender = db.Column(db.Text, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    user = db.relationship('User')

    mealplans = db.relationship(
        'Mealplan',
        backref="clients") 

    
class Mealplan(db.Model):
    """Mealplan for single client"""

    __tablename__ = 'mealplans'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer,
            db.ForeignKey('clients.id'))
    food_id = db.Column(db.Integer,
            db.ForeignKey('foods.id'))
    notes = db.Column(db.Text, nullable=False)

    client = db.relationship('Client')
    
    foods = db.relationship(
        'Food',
        backref="mealplans")

class Food(db.Model):
    """datas food search"""

    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key=True)
    food = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    vitamin_id = db.Column(db.Integer, 
            db.ForeignKey('vitamins.id'))

    mealplan = db.relationship('Mealplan')

    nutrition = db.relationship(
        "Nutrition",
        backref="foods")

    vitamin = db.relationship(
        "Vitamin",
        backref="foods")

class Nutrition(db.Model):
    """food nutrition """

    __tablename__ = 'nutritions'

    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer,
            db.ForeignKey('foods.id'))
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Integer, nullable=False)
    

    food = db.relationship('Food')

class Vitamin(db.Model):
    """food vitamin"""

    __tablename__ = "vitamins"

    id = db.Column(db.Integer, primary_key=True)
    vitamin_A = db.Column(db.Integer, nullable=False)
    vitamin_B = db.Column(db.Integer, nullable=False)
    vitamin_C = db.Column(db.Integer, nullable=False)
    vitamin_E = db.Column(db.Integer, nullable=False)
    vitamin_K = db.Column(db.Integer, nullable=False)
    vitamin_B1 = db.Column(db.Integer, nullable=False)
    vitamin_B2 = db.Column(db.Integer, nullable=False)
    vitamin_B3 = db.Column(db.Integer, nullable=False)

    food = db.relationship(
        'Food',
        backref="foods")







