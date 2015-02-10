from bottle import Bottle, request, response
from passlib.hash import sha256_crypt

from app.models.users import User
from app.models import session

from app.utils import check_exist

app = Bottle()
db = session()


@app.route('/', method='POST')
def users():
    username = request.forms.get('username')
    email = request.forms.get('email')
    password = sha256_crypt.encrypt(request.forms.get('password'))

    obj_user = check_exist(User, User.username, username)
    obj_email = check_exist(User, User.email, email)

    if obj_user or obj_email:
        response.status = 406
        return {'status': 'error', 'message': 'username or'
                                        ' email already registered!'}

    data = {
        'username': username,
        'email': email,
        'password': password
    }
    
    user = User(**data)
    db.add(user)
    db.commit()
    return {'status': 'ok', 'message': 'User successfully added.'}
