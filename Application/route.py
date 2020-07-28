from flask import render_template, redirect, url_for, request
from Application import app, db, bcrypt
from Application.models import Posts, Users
from Application.forms import PostForm, RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    postData = Posts.query.all()
    return render_template("home.html", title="Home", post=postData)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for("home"))
    return render_template("login.html", title="Login", form=form)

@app.route("/newpost", methods=["GET", "POST"])
def post():
    form = PostForm()
    if form.validate_on_submit():
        postData = Posts(
            title = form.title.data,
            content = form.content.data,
            author = current_user
        )
        db.session.add(postData)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        print(form.errors)
    return render_template("newpost.html", title="Post", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data)
        user = Users(
            email=form.email.data,
             password=hash_pw,
             first_name=form.first_name.data,
             last_name=form.last_name.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/edit_account")

def edit_account():
    form = UpdateAccountForm()
    if form.validate_on_submit:
        current_user.first_name = form.first_name.data
        current_user.last_name = form.first_name.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for("edit_account"))
    elif request.method == "GET":
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    return render_template("edit_account.html", title="Edit Account", name=current_user.first_name, form=form)

