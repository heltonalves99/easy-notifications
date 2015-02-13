import json

from redis import StrictRedis
from bottle import Bottle, request
from app.utils import authenticated
from app.models import session
from app.models.devices import Device
from app.models.certificates import Certificate

app = Bottle()
db = session()
redis_db = StrictRedis()


def add_notification(certificate, devices, payload):
    json_message = {
        'devices': devices,
        'payload': payload
    }
    json_message = json.dumps(json_message)
    redis_db.publish(certificate.token, json_message)


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

    if errors:
        return {'not_registered': not_registered,
                'errors': errors}

    if devices:
        add_notification(certificate, devices, payload)

    return {'message': 'Pushs sent to apple, see the web console to errors.',
            'not_registered': not_registered}
