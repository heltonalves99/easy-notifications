# -*- coding: utf-8 -*-
from bottle import request, redirect
from bottle.ext.mongo import MongoPlugin
from passlib.apps import custom_app_context as pwd_context


mongo_client = MongoPlugin(uri="mongodb://127.0.0.1",
                           db="easy_notifications",
                           json_mongo=True,
                           keyword='db').get_mongo()


def authenticated(func):
    def wrapper(db, *args, **kwargs):
        session = request.environ.get('beaker.session')

        if 'email' in session:
            return func(db, *args, **kwargs)

        redirect('/auth/login')
    return wrapper


def check_login(email, password):
    user = mongo_client['users'].find_one({'email': email})
    if user:
        if pwd_context.verify(password, user['password']):
            return True, user
        return False, {'error': 'incorrect password'}
    else:
        return False, {'error': 'email don\'t registered'}


def get_user(email=None, uid=None):
    if email:
        query = {'email': email}
    elif uid:
        query = {'_id': uid}
    else:
        return None
    return mongo_client['users'].find_one(query)
