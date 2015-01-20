
from bottle import Bottle, redirect, request
from bottle import jinja2_template as template
from bottle.ext.mongo import MongoPlugin
from passlib.apps import custom_app_context as pwd_context
from utils import check_login, get_user

app = Bottle()

mongo = MongoPlugin(uri="mongodb://127.0.0.1",
                    db="easy_notifications",
                    json_mongo=True,
                    keyword='db')

app.install(mongo)


@app.get('/')
@app.get('/login')
@app.post('/login')
def login(db):
    if request.method == 'GET':
        return template('dashboard/login')

    email = request.forms.get('email')
    password = request.forms.get('password')

    result = check_login(email, password)

    if result[0]:
        request.session['email'] = result[1]['email']
        redirect('/dashboard')
    else:
        redirect('/auth/login')


@app.route('/logout')
def logout():
    request.session.delete()
    redirect('/auth/login')


@app.get('/register')
@app.post('/register')
def register(db):
    if request.method == 'GET':
        return template('dashboard/register')

    email = request.forms.get('email')
    password = request.forms.get('password')

    if email and password:
        if db['users'].find_one({'email': email}) is not None:
            return {'error': 'email already registered'}
        if db['users'].find_one({'email': email}) is not None:
            return {'error': 'email already registered'}

        user = {
            'email': email,
            'password': pwd_context.encrypt(password)
        }

        uid = db['users'].insert(user)
        request.session['email'] = get_user(uid=uid)['email']
        redirect('/dashboard')
    else:
        redirect('/auth/register')
