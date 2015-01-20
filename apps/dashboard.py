from bottle import Bottle
from bottle import jinja2_template as template

app = Bottle()


@app.get('/')
def pages():
    return template('dashboard/list')
