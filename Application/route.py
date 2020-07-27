from flask import render_template
from Application import app
from Application.models import Posts
from Application.forms import PostForm

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

@app.route("/new-post")
def new_post():
    return render_template("new-post.html")

@app.route("/post")
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
    return render_template("post.html", title="Post", form=form)