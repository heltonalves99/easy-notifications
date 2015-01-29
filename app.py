from bottle import Bottle, run, static_file
from controllers import certificates

app = Bottle()

app.mount('/api/certificates', certificates.app)


@app.route('/assets/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./assets')


run(app, host='localhost', port='8080', debug=True, reloader=True)
