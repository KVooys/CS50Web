with open("db.txt", "r") as dbfile:
    dburl = dbfile.readline()


class Config(object):
    DEBUG = True
    DATABASE_URL = dburl
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    SECRET_KEY = "K7FAQHrEkx"