from bottle import Bottle

from app.models.certificates import Certificate
from app.models.console import Message
from app.utils import authenticated, db

app = Bottle()


@app.route('/', method='GET')
@authenticated
def message(user):
    certs = db.query(Certificate.id).filter(Certificate.user_id == user.id)
    query = db.query(Message).join(Message.certificate).filter(Message.certificate_id.in_(certs))
    data = []

    for item in query:
        dic = item.__dict__
        dic['created_at'] = dic['created_at'].isoformat()
        dic.pop('_sa_instance_state')
        data.append(dic)

    return {'results': data}
