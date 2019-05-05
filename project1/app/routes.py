import requests
from flask import request, render_template, redirect, url_for, abort, jsonify, session
from app import app, db
from app.forms import LoginForm, RegistrationForm
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/")
def index():
    if 'username' in session:
        loginmessage = ('Logged in as ' + session['username'])
        return render_template("index.html", title='Project 1 Home Page ', message=loginmessage)

    else:
        return "You are not logged in <br><a href = '/login'></b>" + \
           "Click here to log in</b></a>"


@app.route("/books")
def books():
    books = db.execute("SELECT * from books ORDER BY title ASC").fetchall()
    return render_template("books.html", title="Books", books=books)


@app.route("/api/<string:isbn>")
def api(isbn):
    book = db.execute("SELECT * from books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        abort(404, "This ISBN is not in the book database.")
    else:
        key = Config.GOODREADS_KEY
        r = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns": book.isbn})
        reviews = r.json()['books'][0]['reviews_count']
        avg_rating = r.json()['books'][0]['average_rating']

        bookjson = {
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "isbn": book.isbn,
            "review_count": reviews,
            "average_score": avg_rating
        }
        return jsonify(bookjson)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session.clear()
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          {"username": form.username.data}).fetchall()
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], form.password.data):
            return "Invalid username and/or password.<a href = '/login'></b>" + "Try again.</b></a>"
        else:
            session["username"] = rows[0]["username"]
            print(session)
            return redirect(url_for('index'))
    else:
        return render_template('login.html', title='Log In', form=form)


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        pw_hash = generate_password_hash(form.password.data)
        data = (form.username.data, form.email.data, pw_hash)
        db.execute("INSERT INTO users (username, email, password_hash) VALUES (:username, :email, :password_hash)",
                   {"username": form.username.data, "email": form.email.data, "password_hash": pw_hash})
        db.commit()
        print("Submission successful!", data)
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

