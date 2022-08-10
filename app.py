from sqlite3 import Cursor
from flask import Flask, render_template, request, flash, redirect, session, g

from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import CreateUserForm, LoginForm, AddClientForm, FoodSearchForm
from models import db, connect_db, User, Client, Mealplan, Food, Nutrition, Vitamin

CURR_USER_KEY = "curr_user"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///mealplan_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)


app.config['SECRET_KEY'] = "DON'T LET THE DOG OUT"


toolbar = DebugToolbarExtension()

#########################################################################
#User signup/login/logout


@app.before_request
def add_user_to_g():
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    
    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    "Logout user."

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/signup', methods=["GET", "POST"])
def sigup():
    """Handle user signup.
    Create new user and add to DB. Redirect to homepage.
    If form not valid. present form.
    If there already is a user with that username: flash message
    and re-present form."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    form = CreateUserForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                firstname=form.firstname.data,
                lastname=form.lastname.data
            )
            
            db.session.commit()

        except IntegrityError:
            flash("Username already exist.", 'danger')
            return render_template('users/signup.html', form=form)
        
        do_login(user)

        return redirect("/")
    
    else: 
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                form.password.data)
            
        if user:
            do_login(user)
            flash(f"Welcome, {user.username}", 'success')
            return redirect("/")
        flash("Invalid password", 'danger')

    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout user."""

    do_logout()
    flash("Success log out!", 'success')

    return redirect("/login") 

##############################################################################
# Messages routes:

@app.route('/clients/new', methods=["GET", "POST"])
def add_client():
    """Add a client:

    Show form if GET. If valid, update client and redirect to user page.
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = AddClientForm()

    if form.validate_on_submit():
        client = Client(
            email=form.email.data,
            name=form.name.data,
            gender=form.gender.data,
            age=form.age.data
            )

        g.user.clients.append(client)
        db.session.commit()

        return redirect("/")

    return render_template('clients/new.html', form=form)


@app.route('/clients/<int:client_id>', methods=["GET"])
def show_client(client_id):
    """Show a client."""

    client = Client.query.get(client_id)
    return render_template('clients/show.html', client=client)


@app.route('/clients/<int:client_id>/delete', methods=["POST"])
def delete_client(client_id):
    """Delete a client."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    client = Client.query.get(client_id)
    if client.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    db.session.delete(client)
    db.session.commit()

    return redirect("/")

##############################################################################
# Homepage and error pages


@app.route('/')
def homepage():
    """Show homepage:
    """

    if g.user:
        clients = (Client.query.all())
        
        return render_template('home.html', clients=clients)

    else:
        return render_template('home-anon.html')

@app.errorhandler(404)
def page_not_foung(e):
    """404 NOT FOUND page"""

    return render_template('404.html'),  404

##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
