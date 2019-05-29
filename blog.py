from flask import Flask, render_template, flash, session, url_for, redirect, jsonify, request, make_response
from sqlite3 import Cursor

from app_forms import MyForm, LoginForm, BlogForm, PostForm
from user_model import User, Product, Blog, Post
from peewee import OperationalError, IntegrityError
from flask_bcrypt import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "vjndbkgnkj.g,nm.dfjbdrgsD437i83u4h.dfjbdrgsD437i83u4h"

@app.route('/', methods=["Get"])
def base():
    return render_template("base.html")

@app.route('/register',methods=["GET","POST"])
def index():
    form = MyForm()
    if form.validate_on_submit():
        #everything is okay
        names = form.names.data
        email = form.email.data
        age = form.age.data
        password = form.password.data
        print("Names {0} Email {1} Age {2}".format(names, email, age))
        password = generate_password_hash(password)
        try:
            User.create(names=names, email=email, age=age, password=password)
            flash("The user was registered successfully ")
            return redirect(url_for("login"))
        except IntegrityError:
            flash("User by {0} email exists".format(email))

    return render_template("index.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        try:
            user = User.get(User.email == email)
            check = check_password_hash(user.password, password)
            print(check)
            if check:
                print("Logged in successfully")
                # return render_template("products.html", user=user)
                session["names"] = user.names
                session["id"] = user.id
                return redirect(url_for("user_blogs"))
            else:
                flash("Wrong username or password")
        except Exception:
            flash("Wrong username or password")
    return render_template("login.html", form=form)

@app.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
    if "names" not in session:
        return redirect(url_for("login"))
    else:
        form = BlogForm()
        if request.method == 'GET':
            return render_template('new_blog.html', form=form)
        else:
            userName = session["names"]
            if form.validate_on_submit():
                title = form.title.data
                description = form.description.data
                user = User.get(User.names == userName)
                try:
                    Blog.create(author=user.names, author_id=user.id, title=title, description=description)
                    flash("The Blog was Added successfully ")
                    return redirect(url_for("user_blogs"))
                except IntegrityError:
                    flash("Blog addition unsuccessful. Ensure the blog title does not exist")

        return render_template("new_blog.html", form=form)


@app.route('/blogs', methods=("GET", "POST"))
def user_blogs():
    if "names" not in session:
        return redirect(url_for("login"))
    else:
        userId = session["id"]
        userName = session["names"]
        blogs_list = []
        blog_items = []
        try:
            blogs = Blog.select()
            for blog in blogs:

                blogs_list.append({"id": blog.id, "title": blog.title, "author": blog.author, "author_id":blog.author_id,
                                   "description": blog.description, "date_added": blog.date_added})

            blog_items = [item for item in blogs_list if item['author'] == userName]
            print(userId)
            print(userName)
        except Exception:
            return make_response(create_new_blog())
        if "names" not in session:
            return redirect(url_for("login"))
        else:
            return render_template("user_blogs.html", blogs=blog_items, author=userName)
15
@app.route('/posts/new/<string:blog_id>', methods=['POST', 'GET'])
def create_new_post(blog_id):
    if "names" not in session:
        return redirect(url_for("login"))
    else:
        form = PostForm()
        if request.method == 'GET':
            return render_template('new_post.html', blog_id=blog_id, form=form)
        else:
            userName = session["names"]
            if form.validate_on_submit():
                title = form.title.data
                content = form.content.data
                user = User.get(User.names == userName)
                try:
                    Post.create(blog_id=blog_id, title=title, content=content, author=user.names)
                    flash("The Post was Added successfully ")
                    return make_response(blog_posts(blog_id))
                except IntegrityError:
                    flash("Post addition unsuccessful. Ensure the post title does not exist")


@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    # print(blog_id)
    posts_list = []
    blog = Blog.get(Blog.id == blog_id)
    blog_title = blog.title
    try:
        posts = Post.select()
        for post in posts:
            posts_list.append({"id":post.id, "title": post.title, "author": post.author, "blog_id": post.blog_id ,
                               "content": post.content, "date_added": post.date_added})

        post_items = [item for item in posts_list if item['blog_id'] == blog_id]
    except Exception:
        return make_response((create_new_post(blog_id)))
    if "names" not in session:
        return redirect(url_for("login"))
    else:
        print(blog_id)
        return render_template("posts.html", posts=post_items, blog_id=blog_id, blog_title=blog_title)

@app.route("/blogs/delete/<string:id>", methods=["GET", "POST", "DELETE"])
def delete_blog(id):
    blog = Blog.get(Blog.id == id)
    blog.delete_instance()
    return redirect(url_for("user_blogs"))


@app.route("/posts/delete/<string:blog_id>/<string:id>", methods=["GET", "POST", "DELETE"])
def delete_post(id, blog_id):
    post = Post.get(Post.id == id)
    post.delete_instance()
    return make_response((blog_posts(blog_id)))


@app.route('/logout')
def logout():
    session.pop("names")
    session.pop("id")
    return redirect(url_for("login"))

if __name__ == '__main__':
    #User.drop_table()
    try:
        Product.create_table()
    except OperationalError:
        pass

    try:
        User.create_table()
    except OperationalError:
        pass

    try:
        Blog.create_table()
    except OperationalError:
        pass

    try:
        Post.create_table()
    except OperationalError:
        pass
    app.run(port=8000)

    #host="0.0.0.0" port=8000
