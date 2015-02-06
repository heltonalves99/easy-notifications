import json

from bottle import Bottle, request
from app.utils import authenticated
from app.models import session

app = Bottle()
db = session()


@app.route('/', method='POST')
@authenticated
def notify():
    errors = []
    tokens = request.forms.getlist('tokens')
    payload = request.forms.get('payload')

    try:
        payload = json.loads(payload)
    except Exception:  # catching any Exception because don't raises ValueError. :(
        errors.append('Payload must be a valid json.')

    if len(tokens) == 0:
        errors.append('Tokens need at least one item.')

    if len(errors) > 0:
        return {'error': errors}

    return {'status': 'ok'}
