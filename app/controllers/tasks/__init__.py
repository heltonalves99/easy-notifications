import json

from redis import StrictRedis
from apnsclient import Message, APNs, Session

redis_db = StrictRedis()


def send_notifications(certificate):
    ps = redis_db.pubsub()
    ps.subscribe(certificate.token)
    apns_session = Session()

    for push in ps.listen():
        if push['type'] == 'message':
            con = apns_session.get_connection(certificate.cert_type,
                                              cert_string=certificate.cert_pem,
                                              key_string=certificate.key_pem)

            push_data = json.loads(push['data'])
            devices = push_data['devices']
            payload = push_data['payload']

            message = Message(devices, **payload)

            # Send the message.
            srv = APNs(con)
            try:
                res = srv.send(message)
            except Exception as e:
                print e
            else:
                # Check failures. Check codes in APNs reference docs.
                for token, reason in res.failed.items():
                    code, errmsg = reason
                    # according to APNs protocol the token reported here
                    # is garbage (invalid or empty), stop using and remove it.
                    print "Device failed: {0}, reason: {1}".format(token, errmsg)

                # Check failures not related to devices.
                for code, errmsg in res.errors:
                    print "Error: {}".format(errmsg)

                # Check if there are tokens that can be retried
                if res.needs_retry():
                    pass
                    # repeat with retry_message or reschedule your task
                    # retry_message = res.retry()
