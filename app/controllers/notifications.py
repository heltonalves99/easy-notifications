import json

from bottle import Bottle, request
from apnsclient import Message, APNs
from app.utils import authenticated
from app.models import session
from app.models.devices import Device
from app.models.certificates import Certificate
from . import apns_session

app = Bottle()
db = session()


def send_notification(certificate, devices, payload):
    con = apns_session.get_connection(certificate.cert_type,
                                      cert_string=certificate.cert_pem,
                                      key_string=certificate.key_pem)

    message = Message(devices, alert="My message", badge=20)

    # Send the message.
    srv = APNs(con)
    try:
        res = srv.send(message)
    except:
        print "Can't connect to APNs, looks like network is down"
    else:
        # Check failures. Check codes in APNs reference docs.
        for token, reason in res.failed.items():
            code, errmsg = reason
            # according to APNs protocol the token reported here
            # is garbage (invalid or empty), stop using and remove it.
            print "Device failed: {0}, reason: {1}".format(token, errmsg)

        # Check failures not related to devices.
        for code, errmsg in res.errors:
            print "Error: {}".format(errmsg)

        # Check if there are tokens that can be retried
        if res.needs_retry():
            # repeat with retry_message or reschedule your task
            retry_message = res.retry()
    return True


@app.route('/', method='POST')
@authenticated
def notify():
    devices = []
    not_registered = []
    errors = []
    tokens = request.forms.getlist('tokens')
    cert_token = request.forms.get('cert_token')
    payload = request.forms.get('payload')

    try:
        payload = json.loads(payload)
    except Exception:  # catching any Exception because don't raises ValueError. :(
        errors.append('Payload must be a valid json.')

    certificate = db.query(Certificate).filter(Certificate.token == cert_token).first()

    if not certificate:
        errors.append('Certificate token invalid.')
        return {'errors': errors}

    if not tokens:
        errors.append('Tokens need at least one item.')

    for token in tokens:
        device = db.query(Device).filter(Device.token == token).first()
        if device:
            devices.append(token)
        else:
            not_registered.append(token)

    if devices:
        send_notification(certificate, devices, payload)

    if errors:
        return {'error': errors}

    return {'message': 'Push notification delivered.',
            'devices': devices,
            'not_registered': not_registered}
