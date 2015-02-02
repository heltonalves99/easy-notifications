from bottle import Bottle, request
from passlib.hash import sha256_crypt
from plugins import sql_plugin

from models.users import User

app = Bottle()
app.install(sql_plugin())


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
