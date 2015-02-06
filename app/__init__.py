from bottle import Bottle, static_file
from app.controllers import users, certificates, devices, notifications

main = Bottle()

main.mount('/api/users', users.app)
main.mount('/api/devices', devices.app)
main.mount('/api/certificates', certificates.app)
main.mount('/api/notifications', notifications.app)


@main.route('/assets/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./assets')
