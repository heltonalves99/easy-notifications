from redis import StrictRedis
from bottle import run
from app import main
from app.controllers.tasks import PushListener
from app.models import session
from app.models.certificates import Certificate
from app.settings import DEBUG

db = session()
redis_db = StrictRedis()


def connect_apns():
    certificates = db.query(Certificate).all()

    # start certificates threads
    for cert in certificates:
        listener = PushListener(cert)
        listener.start()

if __name__ == '__main__':
    connect_apns()
    run(main, host='localhost', port='8080', debug=DEBUG)
