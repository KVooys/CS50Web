from flask import Flask
from flask_session import Session
from config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.config.from_object(Config)
Session(app)

# Set up database
engine = create_engine(Config.DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))


from app import routes
