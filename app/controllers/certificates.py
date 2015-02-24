from bottle import Bottle, request

from app.models.certificates import Certificate
from app.models import db
from app.utils import authenticated, generate_token, paginate

app = Bottle()


@app.route('/', method='GET')
@app.route('/<page:int>', method='GET')
@authenticated
def certificates(user, page=1):
    query = db.query(Certificate).filter(Certificate.user == user)
    pagination = paginate(query=query, page=page)

    data = []
    for item in pagination['results']:
        dict = item.__dict__
        dict.pop('_sa_instance_state')
        data.append(dict)

    pagination['results'] = data
    return pagination


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
