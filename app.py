from bottle import route, run, template


@route('/')
def index():
    return template('base')

run(host='localhost', port='8080', debug=True)
