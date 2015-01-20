from bottle import Bottle
from bottle import jinja2_template as template

app = Bottle()


@app.get('/<page>')
def pages(page):
    return template('dashboard/{}'.format(page))
