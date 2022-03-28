import pdb
from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db ,User
from forms import UserForm, ClearForm, LoginForm
from sqlalchemy.exc import IntegrityError



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

debug = DebugToolbarExtension(app)
connect_db(app)



@app.route('/')
def home_page():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def signup():

    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        new_user = User.register(username, password, email, first_name, last_name)
        
        db.session.add(new_user)

        session['username'] = new_user.username


        db.session.commit()
        
        flash('Welcome! Successfully Created Your Account!', "success",)

        
        return redirect(f'/users/{new_user.username}')
    else:
         return render_template('index.html', form=form)




# @app.route('/users/<username>')
# def display_user(username):
#     """Displays specific user"""
    
#     if "username" not in session:
#         return redirect('/register')
#     elif session['username'] != username:
#         flash('You were not authorized to use that page')
#         redirect ('/home_page')

#     user = User.query.get(username)
#     form = ClearForm()

@app.route('/login', methods=["GET", "POST"])
def login():

    session.clear()

    form = LoginForm()

    users = User.query.all()

    if form.validate_on_submit():
        username = form.username.data
        pw = form.password.data

        user = User.authenticate(username, pw)
        

        if user:
            
            session['username'] = user.username
            username = session['username']
            return redirect(f"/users/{user.username}")
        else:
            flash('invalid username and password combination')
            form.username.errors = ["Invalid username/password."]
            return redirect('/login', form=form)
    
    return render_template('login.html', form=form, users=users)

@app.route('/users/<username>')
def show_user_homepage(username):

    user = User.query.get(username)

    
    form = ClearForm()

    return render_template('loggedin.html', form=form, user=user)

