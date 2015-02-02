from bottle import Bottle, request, parse_auth
from plugins import sqlplugin

from models.users import User
from models.certificates import Certificate
from utils import check_pass, authenticated

app = Bottle()
app.install(sqlplugin)


@app.route('/', method='GET')
@authenticated
def certificates(db):
    auth = request.headers.get('Authorization')
    username, password = parse_auth(auth)

    user = db.query(User).filter(User.username == username).first()

    query = db.query(Certificate).filter(Certificate.user_id == user.id)
    data = []
    for item in query:
        dict = item.__dict__
        dict.pop('_sa_instance_state')
        data.append(dict)
    return {'results': data}


@app.route('/', method='POST')
@authenticated
def add_certificates(db):
    auth = request.headers.get('Authorization')
    username, password = parse_auth(auth)

    user = db.query(User).filter(User.username == username).first()

    data = {
        'user_id': user.id,
        'platform': request.forms.get('platform'),
        'type': request.forms.get('type'),
        'name': request.forms.get('name'),
        'cert_pem': request.forms.get('cert_pem'),
        'key_pem': request.forms.get('key_pem')
    }
    certificate = Certificate(**data)
    db.add(certificate)
    return data
