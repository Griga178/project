from flask import render_template, url_for, request
from .models import *

@app.route('/')
@app.route('/main')
def main():

    return render_template('main.html')
