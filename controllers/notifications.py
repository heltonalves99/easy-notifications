from bottle import Bottle, request
from plugins import sql_plugin
from utils import authenticated

app = Bottle()
app.install(sql_plugin())


@app.route('/', method='POST')
@authenticated
def notify(db):
    data = {
        'devices': request.forms.getall('devices'),
        'payload': request.forms.get('payload')
    }
    return data
