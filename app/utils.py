import string
import random

from bottle import request, response, parse_auth
from passlib.hash import sha256_crypt
from app.models.users import User
from app.models import session

db = session()


def authenticated(func):
    def wrapper(*args, **kwargs):
        check = check_pass()
        if check[0]:
            return func(check[1], *args, **kwargs)
        response.status = 401
        return {'status': 'error', 'message': 'Error with auth data provided.'}
    return wrapper


def check_pass():
    auth = request.headers.get('Authorization')

    if not auth:
        return False

    username, password = parse_auth(auth)
    user = db.query(User).filter(User.username == username).first()
    return sha256_crypt.verify(password, user.password), user


def check_exist(model, key, value):
    obj = db.query(model).filter(key == value).first()
    if obj:
        return obj
    return None


def generate_token(size=20, chars=string.ascii_uppercase + string.digits):
    """
        from: http://stackoverflow.com/a/2257449/492161
    """
    return ''.join(random.choice(chars) for _ in range(size))
