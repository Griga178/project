from flask import Flask

from settings import DATA_BASE_PATH
app = Flask(__name__, template_folder = "templates")

app.config['SECRET_KEY'] = 'AASDFASDF'
app.config['SQLALCHEMY_DATABASE_URI'] = DATA_BASE_PATH
app.debug =  True
