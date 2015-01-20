from bottle import Bottle, run, static_file
from beaker.middleware import SessionMiddleware
from apps import dashboard, api, auth

app = Bottle()

app.mount('/api', api.app)
app.mount('/auth', auth.app)
app.mount('/dashboard', dashboard.app)


@app.route('/assets/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./assets')

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': True,
    'session.data_dir': './data_sessions',
    'session.auto': True
}

session_app = SessionMiddleware(app, session_opts)

run(session_app, host='localhost', port='8080', debug=True, reloader=True)
