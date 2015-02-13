from redis import StrictRedis
from rq import Queue, cancel_job
from bottle import run
from app import main
from app.controllers.tasks import send_notifications
from app.models import session
from app.models.certificates import Certificate

db = session()
redis_db = StrictRedis()


def reconnect_apns():
    certificates = db.query(Certificate).all()
    queue = Queue('pushs', connection=redis_db)

    # clearing connections
    for job in queue.job_ids:
        cancel_job(job, connection=redis_db)

    # reconnecting
    for cert in certificates:
        queue.enqueue(send_notifications, cert)

if __name__ == '__main__':
    reconnect_apns()
    run(main, host='localhost', port='8080', debug=True, reloader=True)
