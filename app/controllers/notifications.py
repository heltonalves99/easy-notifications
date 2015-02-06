import json

from bottle import Bottle, request
from app.utils import authenticated
from app.models import session

app = Bottle()
db = session()


@app.route('/', method='POST')
@authenticated
def notify():
#    try:
#        payload = json.loads(request.forms.get('payload'))
#    except ValueError:
#        return {'error': 'Payload must be a valid json.'}
    payload = {}
    data = {
        'tokens': request.forms.getall('tokens'),
        'payload': payload
    }

    return data
