from bottle import request, parse_auth
from passlib.hash import sha256_crypt
from models.users import User


def authenticated(func):
    def wrapper(db, *args, **kwargs):
        if check_pass(db):
            return func(db, *args, **kwargs)
        return {'status': 'error', 'message': 'Error with auth data provided.'}
    return wrapper


def check_pass(db):
    auth = request.headers.get('Authorization')

    if not auth:
        return False

    username, password = parse_auth(auth)
    user = db.query(User).filter(User.username == username).first()
    return sha256_crypt.verify(password, user.password)
