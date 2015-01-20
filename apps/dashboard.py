from bottle import Bottle
from bottle import jinja2_template as template

app = Bottle()


@app.get('/login')
def login():
    return template('dashboard/login')
