import json

from bottle import Bottle, request
from app.utils import authenticated
from app.models import session
from app.models.devices import Device

app = Bottle()
db = session()


def send_notification(device, payload):
    return True


@app.route('/', method='POST')
@authenticated
def notify():
    devices = []
    errors = []
    tokens = request.forms.getlist('tokens')
    payload = request.forms.get('payload')

    try:
        payload = json.loads(payload)
    except Exception:  # catching any Exception because don't raises ValueError. :(
        errors.append('Payload must be a valid json.')

    if len(tokens) == 0:
        errors.append('Tokens need at least one item.')
        return {'error': errors}

    for token in tokens:
        device = db.query(Device).filter(Device.token == token).first()
        if device:
            send_notification(device, payload)
            devices.append(device.id)
        else:
            errors.append('Device token does not exist.')

    if len(errors) > 0:
        return {'error': errors}

    return {'message': 'Push notification delivered.',
            'devices': devices}
