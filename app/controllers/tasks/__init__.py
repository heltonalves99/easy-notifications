import json
import threading

from datetime import datetime
from redis import StrictRedis
from apnsclient import Message, APNs, Session

from app.models import session
from app.models.devices import Device
from app.models.console import Message as LogMessage

db = session()


class PushListener(threading.Thread):
    def __init__(self, certificate):
        threading.Thread.__init__(self)

        self.redis = StrictRedis()
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(certificate.token)

        self.apns_session = Session()
        self.certificate = certificate

    def _log_it(self, message):
        msg = {
            'certificate': self.certificate,
            'log': message,
            'created_at': datetime.now()
        }

        log = LogMessage(**msg)
        db.add(log)
        db.commit()

    def _send_notification(self, apns_message):
        con = self.apns_session.get_connection(self.certificate.cert_type,
                                               cert_string=self.certificate.cert_pem,
                                               key_string=self.certificate.key_pem)

        # Send the message.
        srv = APNs(con)
        try:
            res = srv.send(apns_message)
        except Exception as e:
            print e
        else:
            # Check failures. Check codes in APNs reference docs.
            for token, reason in res.failed.items():
                code, errmsg = reason
                # according to APNs protocol the token reported here
                # is garbage (invalid or empty), stop using and remove it
                # Log it!
                log_message = "Device failed: {0}, reason: {1}".format(token, errmsg)
                self._log_it(log_message)

                # inactive device token
                t = db.query(Device).filter(Device.token == token).first()
                t.status = False
                db.commit()

            # Check failures not related to devices.
            for code, errmsg in res.errors:
                log_message = "Error: {}".format(errmsg)
                self._log_it(log_message)

            # Check if there are tokens that can be retried
            if res.needs_retry():
                # repeat with retry message
                self._send_notification(res.retry())

    def run(self):
        for item in self.pubsub.listen():
            if item['type'] == "message":
                data = json.loads(item['data'])
                devices = data['devices']
                payload = data['payload']

                apns_message = Message(devices, **payload)

                self._send_notification(apns_message)
