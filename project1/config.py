with open("db.txt", "r") as dbfile:
    dburl = dbfile.readline()

with open("goodreads.txt", "r") as file:
    gr_key = file.readline()


class Config(object):
    DEBUG = True
    DATABASE_URL = dburl
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    SECRET_KEY = "K7FAQHrEkx"
    GOODREADS_KEY = gr_key
