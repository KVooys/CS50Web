import requests
from flask import render_template, flash, redirect, url_for, abort, jsonify
from app import app, db
from app.forms import LoginForm
from config import Config


@app.route("/")
def index():
    return render_template("index.html", title='Project 1 Home Page')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Log In', form=form)


@app.route("/books")
def books():
    books = db.execute("SELECT * from books ORDER BY title ASC").fetchall()
    return render_template("books.html", title="Books", books=books)


@app.route("/book/<int:book_id>")
def book(book_id):
    book = db.execute("SELECT * from books WHERE book_id = :book_id", {"book_id": book_id}).fetchone()
    if book is None:
        abort(404, "This book is not in the book database")
    else:
        return render_template("book.html", title="Book", book=book)


@app.route("/api/<isbn>")
def isbn(isbn):
    book = db.execute("SELECT * from books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        abort(404, "This IBN is not in the book database.")
    else:
        key = Config.GOODREADS_KEY
        r = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns": book.isbn})
        print(r.json()['books'][0])
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
