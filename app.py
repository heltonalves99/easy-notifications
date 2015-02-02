from bottle import Bottle, run, static_file
from controllers import users, certificates, devices

main = Bottle()

main.mount('/api/users', users.app)
main.mount('/api/devices', devices.app)
main.mount('/api/certificates', certificates.app)


@main.route('/assets/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./assets')

if __name__ == '__main__':
    run(main, host='localhost', port='8080', debug=True, reloader=True)
