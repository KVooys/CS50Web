import csv
import json
import psycopg2

# read psql variables
with open("db.json", "r") as dbfile:
    dbjson = json.load(dbfile)
    db_host = dbjson['host']
    db_database = dbjson['database']
    db_user = dbjson['user']
    db_password = dbjson['password']


def read_csv():
    with open("test.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        # syntax of the csv:
        # isbn,title,author,year
        for row in reader:
            print(row['isbn'], row['title'], row['author'], row['year'])


def test_connect_to_db():
    conn = None
    try:
        conn = psycopg2.connect(host=db_host, database=db_database, user=db_user, password=db_password)
        cur = conn.cursor()
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def create_book_table():
    conn = None
    try:
        conn = psycopg2.connect(host=db_host, database=db_database, user=db_user, password=db_password)
        cur = conn.cursor()
        test_table = """CREATE TABLE if not exists books (
                    book_id SERIAL PRIMARY KEY,
                    isbn TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year INTEGER NOT NULL     
                )"""
        cur.execute(test_table)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def add_books_to_table():
    conn = None
    try:
        conn = psycopg2.connect(host=db_host, database=db_database, user=db_user, password=db_password)
        cur = conn.cursor()

        # use csv file to build the insert statements
        with open("books.csv") as csvfile:
            reader = csv.DictReader(csvfile)
            # syntax of the csv:
            # isbn,title,author,year
            for row in reader:
                booktuple = ((row['isbn'], row['title'], row['author'], row['year']))
                print(booktuple)
                cur.execute("INSERT INTO books (isbn, title, author, year) VALUES(%s, %s, %s, %s)", booktuple)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def read_books_from_table():
    conn = None
    try:
        conn = psycopg2.connect(host=db_host, database=db_database, user=db_user, password=db_password)
        cur = conn.cursor()
        cur.execute("SELECT count(*) from books")
        row = cur.fetchone()
        while row is not None:
            print(row)
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def drop_book_table():
    conn = None
    try:
        conn = psycopg2.connect(host=db_host, database=db_database, user=db_user, password=db_password)
        cur = conn.cursor()
        cur.execute("DROP TABLE books")
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def create_user_table():
    conn = None
    try:
        conn = psycopg2.connect(host=db_host, database=db_database, user=db_user, password=db_password)
        cur = conn.cursor()
        test_table = """CREATE TABLE if not exists users (
                    user_id SERIAL PRIMARY KEY,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password_hash TEXT NOT NULL
                )"""
        cur.execute(test_table)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def read_users_from_table():
    conn = None
    try:
        conn = psycopg2.connect(host=db_host, database=db_database, user=db_user, password=db_password)
        cur = conn.cursor()
        cur.execute("SELECT * from users")
        row = cur.fetchone()
        while row is not None:
            print(row)
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def drop_user_table():
    conn = None
    try:
        conn = psycopg2.connect(host=db_host, database=db_database, user=db_user, password=db_password)
        cur = conn.cursor()
        cur.execute("DROP TABLE users")
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



# read_csv()
# create_book_table()
# add_books_to_table()
# read_books_from_table()
# create_user_table()
read_users_from_table()
# create_sample_user
# drop_book_table()
# drop_user_table()

