from bottle import Bottle, request
from passlib.hash import sha256_crypt

from app.models.users import User
from app.models import session

app = Bottle()
db = session()


@app.route('/', method='POST')
def users():
    data = {
        'username': request.forms.get('username'),
        'email': request.forms.get('email'),
        'password': sha256_crypt.encrypt(request.forms.get('password'))
    }

    user = User(**data)
    db.add(user)
    db.commit()
    return {'status': 'ok', 'message': 'User successfully added.'}
