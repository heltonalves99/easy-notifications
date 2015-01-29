from bottle import Bottle, request
from plugins import sqlplugin
from models.certificates import Certificate

app = Bottle()
app.install(sqlplugin)


@app.route('/', method='GET')
def certificates(db):
    query = db.query(Certificate).all()
    data = []
    for item in query:
        dict = item.__dict__
        dict.pop('_sa_instance_state')
        data.append(dict)
    return {'results': data}


@app.route('/', method='POST')
def add_certificates(db):
    data = {
        'user_id': request.forms.get('user_id'),
        'platform': request.forms.get('platform'),
        'type': request.forms.get('type'),
        'name': request.forms.get('name'),
        'cert_pem': request.forms.get('cert_pem'),
        'key_pem': request.forms.get('key_pem')
    }
    certificate = Certificate(**data)
    db.add(certificate)
    return data
