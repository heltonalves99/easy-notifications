from bottle import Bottle, request, parse_auth
from plugins import sqlplugin

from models.certificates import Certificate
from models.devices import Device
from models.users import User
from utils import authenticated

app = Bottle()
app.install(sqlplugin)


@app.route('/', method='GET')
@authenticated
def devices(db):  # improve this, please! :(
    auth = request.headers.get('Authorization')
    username, password = parse_auth(auth)

    user = db.query(User).filter(User.username == username).first()

    query = db.query(Certificate).filter(Certificate.user_id == user.id)
    data = []
    for item in query:
        for device in item.devices:
            data.append(device)
    return {'results': data}


@app.route('/', method='POST')
@authenticated
def add_devices(db):
    data = {
        'certificate_id': request.forms.get('certificate'),
        'name': request.forms.get('name'),
        'token': request.forms.get('token'),
        'status': True
    }
    device = Device(**data)
    db.add(device)
    return data
