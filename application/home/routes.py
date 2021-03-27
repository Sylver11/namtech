from application.home import bp as home
from flask import render_template

@home.route('/', methods=['GET'])
def index():
    return render_template('home_bp/index.html')
