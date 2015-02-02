from bottle import Bottle, request, parse_auth
from plugins import sql_plugin

from models.certificates import Certificate
from models.devices import Device
from models.users import User
from utils import authenticated

app = Bottle()
app.install(sql_plugin())


@app.route('/', method='GET')
@authenticated
def devices(db):
    auth = request.headers.get('Authorization')
    username, password = parse_auth(auth)

    user = db.query(User).filter(User.username == username).first()

    certs = db.query(Certificate.id).filter(Certificate.user_id == user.id)
    query = db.query(Device).join(Device.certificate).filter(Device.certificate_id.in_(certs))
    data = []

    for item in query:
        dict = item.__dict__
        dict.pop('_sa_instance_state')
        data.append(dict)

    return {'results': data}


@app.route('/', method='POST')
@authenticated
def add_devices(db):
    cert_pk = int(request.forms.get('certificate'))
    cert = db.query(Certificate).filter(Certificate.id == cert_pk).first()
    data = {
        'certificate': cert,
        'name': request.forms.get('name'),
        'token': request.forms.get('token'),
        'status': True
    }
    device = Device(**data)
    db.add(device)
    data.pop('certificate')
    data['certificate_id'] = cert_pk
    return data
