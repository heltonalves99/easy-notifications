from bottle import Bottle, request, redirect
from bottle import jinja2_template as template
from bottle.ext.mongo import MongoPlugin
from utils import authenticated

dashboard_app = Bottle()

mongo = MongoPlugin(uri="mongodb://127.0.0.1",
                    db="easy_notifications",
                    json_mongo=True,
                    keyword='db')

dashboard_app.install(mongo)


@dashboard_app.get('/')
@authenticated
def home(db):
    return template('dashboard/base_dashboard')


@dashboard_app.get('/certificates')
@authenticated
def certificates(db):
    certs = db['certificates'].find({'user': request.current_user['_id']})
    return template('dashboard/certificates', title='Certificates', certificates=certs)


@dashboard_app.get('/certificates/add')
@dashboard_app.post('/certificates/add')
@authenticated
def certificates_add(db):
    if request.method == 'GET':
        return template('dashboard/certificates_form', title='Certificates')

    # need validation
    db['certificates'].insert({
        'user': request.current_user['_id'],
        'platform': request.forms.get('platform'),
        'type': request.forms.get('type'),
        'name': request.forms.get('name'),
        'cert_pem': request.forms.get('cert_pem'),
        'cert_key': request.forms.get('cert_key'),
        'devices': 0
    })

    redirect('/dashboard/certificates')


@dashboard_app.get('/devices')
@authenticated
def devices(db):
    return template('dashboard/list', title='Devices')
