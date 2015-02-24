from bottle import Bottle

from app.models.certificates import Certificate
from app.models.console import Message
from app.models import db
from app.utils import authenticated, paginate

app = Bottle()


@app.route('/', method='GET')
@app.route('/<page:int>', method='GET')
@authenticated
def message(user, page=1):
    certs = db.query(Certificate.id).filter(Certificate.user_id == user.id)
    query = db.query(Message).join(Message.certificate).filter(Message.certificate_id.in_(certs))

    pagination = paginate(query=query, page=page)
    data = []
    for item in pagination['results']:
        dic = item.__dict__
        dic['created_at'] = dic['created_at'].isoformat()
        dic.pop('_sa_instance_state')
        data.append(dic)

    pagination['results'] = data

    return pagination
