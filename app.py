from bottle import Bottle, run, request
from bottle.ext.mongo import MongoPlugin

app = Bottle()

mongo = MongoPlugin(uri="mongodb://127.0.0.1",
                    db="easy_notifications",
                    json_mongo=True,
                    keyword='db')

app.install(mongo)


@app.post('/api/device')
def add_device(db):
    token = request.forms.get('token', None)
    if token:
        id = db['devices'].insert({'device': token})
        return {'id': str(id)}
    return {'error': '"token" is required.'}


run(app, host='localhost', port='8080', debug=True, reloader=True)
