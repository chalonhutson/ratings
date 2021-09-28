"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db




app = Flask(__name__)


# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route("/users")
def user_list():
    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/register", methods = ["POST"])
def register_user():
    email = request.form["email"]
    password = request.form["password"]
    password_confirm = request.form["password-confirm"]
    age = request.form["age"]
    zipcode = request.form["zipcode"]

    if password != password_confirm:
        flash("RIP, your passwords don't match.")
        return render_template("homepage.html")
    else:
        user = User(email = email, password = password, age = age, zipcode = zipcode)
        db.session.add(user)
        db.session.commit()
        flash("You added a user.")
        return render_template("homepage.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    if User.query.filter_by(email=email):
        query = User.query.filter_by(email = email)
        results = query.first()
        if results.password == password:
            flash("Login successful.")
            return render_template("homepage.html")
        else:
            flash("Incorrect password.")
            return render_template("homepage.html")
    else:
        flash("Incorrect username.")
        return render_template("homepage.html")




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
