from bottle import Bottle, request
from passlib.hash import sha256_crypt
from plugins import sqlplugin

from models.users import User

app = Bottle()
app.install(sqlplugin)


@app.route('/', method='POST')
def users(db):
    data = {
        'username': request.forms.get('username'),
        'email': request.forms.get('email'),
        'password': sha256_crypt.encrypt(request.forms.get('password'))
    }

    user = User(**data)
    db.add(user)
    return {'status': 'ok', 'message': 'User successfully added.'}
