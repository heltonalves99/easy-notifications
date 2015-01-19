from bottle import Bottle, run, static_file
from bottle.ext.mongo import MongoPlugin
from apps import dashboard, api

app = Bottle()

mongo = MongoPlugin(uri="mongodb://127.0.0.1",
                    db="easy_notifications",
                    json_mongo=True,
                    keyword='db')

app.install(mongo)
app.mount('/dashboard', dashboard.app)
app.mount('/api', api.app, skip=None)


@app.route('/assets/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./assets')

run(app, host='localhost', port='8080', debug=True, reloader=True)
