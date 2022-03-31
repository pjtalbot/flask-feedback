from crypt import methods
import pdb
from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db ,User, Feedback
from forms import FeedbackForm, UserForm, ClearForm, LoginForm
from sqlalchemy.exc import IntegrityError


# add Unauthorized()
# make 404
# add """""" docs
# practice making tests?
# organize templates / rename


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

@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users)

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

@app.route('/feedback/new', methods=["GET", "POST"])
def show_feedback_form():
    form = FeedbackForm()

    if not session['username']:
        redirect ('/login')

    elif form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        username = session['username']

        new_feedback = Feedback(title=title, content=content, username=username)

        db.session.add(new_feedback)
        db.session.commit()

        return redirect(f'/users/{username}')


    return render_template('new_feedback.html', form=form)

# @app.route('/feedback/new', methods=["POST"])
# def create_feedback():





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

    # session.clear()

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

@app.route("/logout")
def logout():
    """Logout route."""

    # use pop? or is another session method better?

    session.pop("username")
    return redirect("/login")

@app.route("/feedback/<int:feedback_id>", methods=["GET", "POST"])
def display_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)

    return render_template('feedback.html', feedback=feedback)

@app.route("/feedback/<int:feedback_id>/edit", methods=["GET", "POST"])
def edit_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f'/feedback/{feedback.id}')

    return render_template('feedback_edit.html', feedback=feedback, form=form)

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)

    if session['username'] == feedback.username:
        db.session.delete(feedback)
        db.session.commit()
        # add flash message
    return redirect(f'/users/{feedback.username}')

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):

    

    feedback = Feedback.query.filter(Feedback.username == username)

    for f in feedback:

        db.session.delete(f)
    
    db.session.commit()

    user = User.query.get(username)

    db.session.delete(user)
    db.session.commit()
    
    session.pop('username')

    return redirect('/login')
    
