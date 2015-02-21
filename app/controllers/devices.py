from bottle import Bottle, request, parse_auth

from app.models.certificates import Certificate
from app.models.devices import Device
from app.models.users import User
from app.models import session
from app.utils import authenticated

app = Bottle()
db = session()


@app.route('/', method='GET')
@authenticated
def devices():
    auth = request.headers.get('Authorization')
    username, password = parse_auth(auth)

    user = db.query(User).filter(User.username == username).first()

    certs = db.query(Certificate.id).filter(Certificate.user_id == user.id)
    query = db.query(Device).join(Device.certificate).filter(Device.certificate_id.in_(certs),
                                                             Device.status == True)  # noqa
    data = []

    for item in query:
        dict = item.__dict__
        dict.pop('_sa_instance_state')
        data.append(dict)

    return {'results': data}


@app.route('/', method='POST')
@authenticated
def add_devices():
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
    db.commit()
    data.pop('certificate')
    data['certificate_id'] = cert_pk
    return data
