from bottle import Bottle, run, static_file
from apps import dashboard, api, auth

app = Bottle()

app.mount('/api', api.api_app)
app.mount('/auth', auth.auth_app)
app.mount('/dashboard', dashboard.dashboard_app)


@app.route('/assets/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./assets')


run(app, host='localhost', port='8080', debug=True, reloader=True)
