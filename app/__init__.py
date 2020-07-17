from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'microims-distributed-system'

app.config['MYSQL_DATABASE_USER'] = 'username'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'microims-2'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
db = MySQL(app)

from app import routes