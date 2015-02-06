import json

from bottle import Bottle, request
from plugins import sql_plugin
from utils import authenticated

app = Bottle()
app.install(sql_plugin())


@app.route('/', method='POST')
@authenticated
def notify(db):
    try:
        payload = json.loads(request.forms.get('payload'))
    except ValueError:
        return {'error': 'Payload must be a valid json.'}

    data = {
        'tokens': request.forms.getall('tokens'),
        'payload': payload
    }

    return data
