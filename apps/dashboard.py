from bottle import Bottle
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
    return template('dashboard/list')
