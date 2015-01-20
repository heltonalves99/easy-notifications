# -*- coding: utf-8 -*-
from passlib.apps import custom_app_context as pwd_context
from bottle.ext.mongo import MongoPlugin


mongo_client = MongoPlugin(uri="mongodb://127.0.0.1",
                           db="easy_notifications",
                           json_mongo=True,
                           keyword='db').get_mongo()


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
