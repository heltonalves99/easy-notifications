from bottle import Bottle, request

from app.models.certificates import Certificate
from app.models import db
from app.utils import authenticated, generate_token

app = Bottle()


@app.route('/', method='GET')
@authenticated
def certificates(user):
    query = db.query(Certificate).filter(Certificate.user == user)
    data = []
    for item in query:
        dict = item.__dict__
        dict.pop('_sa_instance_state')
        data.append(dict)
    return {'results': data}


@app.route('/', method='POST')
@authenticated
def add_certificates(user):
    data = {
        'user': user,
        'platform': request.forms.get('platform'),
        'type': request.forms.get('type'),
        'name': request.forms.get('name'),
        'cert_pem': request.forms.get('cert_pem'),
        'key_pem': request.forms.get('key_pem'),
        'token': generate_token()
    }
    certificate = Certificate(**data)
    db.add(certificate)
    db.commit()
    data.pop('user')
    data['user_id'] = user.id
    return data
