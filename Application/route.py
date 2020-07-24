
from flask import render_template
from Application import app
from Application.models import Posts

@app.route("/")
@app.route("/home")
def home():
    postData = Posts.query.first()
    return render_template("home.html", title="Home", post=postData)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

