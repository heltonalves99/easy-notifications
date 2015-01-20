from bottle import Bottle, run, static_file, request
from beaker.middleware import SessionMiddleware
from apps import dashboard, api, auth
from utils import get_user

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': True,
    'session.data_dir': './data_sessions',
    'session.auto': True
}

app = SessionMiddleware(Bottle(), session_opts)

app.wrap_app.mount('/api', api.api_app)
app.wrap_app.mount('/auth', auth.auth_app)
app.wrap_app.mount('/dashboard', dashboard.dashboard_app)


@app.wrap_app.hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']
    request.current_user = None

    if 'email' in request.session:
        request.current_user = get_user(request.session['email'])


@app.wrap_app.route('/assets/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./assets')


run(app, host='localhost', port='8080', debug=True, reloader=True)
