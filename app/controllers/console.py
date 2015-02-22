from bottle import Bottle, request, parse_auth

from app.models.certificates import Certificate
from app.models.console import Message
from app.models.users import User
from app.models import session
from app.utils import authenticated

app = Bottle()
db = session()


@app.route('/', method='GET')
@authenticated
def message():
    auth = request.headers.get('Authorization')
    username, password = parse_auth(auth)

    user = db.query(User).filter(User.username == username).first()

    certs = db.query(Certificate.id).filter(Certificate.user_id == user.id)
    query = db.query(Message).join(Message.certificate).filter(Message.certificate_id.in_(certs))
    data = []

    for item in query:
        dic = item.__dict__
        dic['created_at'] = dic['created_at'].isoformat()
        dic.pop('_sa_instance_state')
        data.append(dic)

    return {'results': data}
