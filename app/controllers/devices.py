from bottle import Bottle, request

from app.models.certificates import Certificate
from app.models.devices import Device
from app.models import db
from app.utils import authenticated, paginate

app = Bottle()


@app.route('/', method='GET')
@app.route('/<page:int>', method='GET')
@authenticated
def devices(user, page=1):
    certs = db.query(Certificate.id).filter(Certificate.user_id == user.id)
    query = db.query(Device).join(Device.certificate).filter(Device.certificate_id.in_(certs),
                                                             Device.status == True)  # noqa

    pagination = paginate(query=query, page=page)

    data = []
    for item in pagination['results']:
        dic = item.__dict__
        dic.pop('_sa_instance_state')
        data.append(dic)

    pagination['results'] = data

    return pagination


@app.route('/', method='POST')
@authenticated
def add_devices(user):
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
