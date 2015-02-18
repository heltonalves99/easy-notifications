import json
import threading

from redis import StrictRedis
from apnsclient import Message, APNs, Session


class PushListener(threading.Thread):
    def __init__(self, certificate):
        threading.Thread.__init__(self)

        self.redis = StrictRedis()
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(certificate.token)

        self.apns_session = Session()
        self.con = self.apns_session.get_connection(certificate.cert_type,
                                                    cert_string=certificate.cert_pem,
                                                    key_string=certificate.key_pem)

    def _send_notification(self, message):
        push_data = json.loads(message)
        devices = push_data['devices']
        payload = push_data['payload']

        _message = Message(devices, **payload)

        # Send the message.
        srv = APNs(self.con)
        try:
            res = srv.send(_message)
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

    def run(self):
        for item in self.pubsub.listen():
            if item['type'] == "message":
                self._send_notification(item['data'])
