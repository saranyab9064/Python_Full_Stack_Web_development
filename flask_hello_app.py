from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgres://sara@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db is instance of our database
# db.model -create and manipulate models,db.session create and manipulate transactions
db = SQLAlchemy(app)

class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable = False)
def __repr__(self):
    return f'<Person ID: {self.id}, name: {self.name}>'
 # detects models and create tables for them(if they don't exist)
db.create_all()

# @app is python decorator
@app.route('/')
# index is std name for route handler
def index():
    person = Person.query.first()
    return'Hello '+ person.name