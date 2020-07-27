from flask import render_template, redirect, url_for
from Application import app, db, bcrypt
from Application.models import Posts, Users
from Application.forms import PostForm, RegistrationForm

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

@app.route("/newpost")
def post():
    form = PostForm()
    if form.validate_on_submit():
        postData = Posts(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            title = form.title.data,
            content = form.content.data
        )
        db.session.add(postData)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        print(form.errors)
    return render_template("newpost.html", title="Post", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data)
        user = Users(email=form.email.data, password=hash_pw)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)