import json
import random
from apns import APNs, Payload
from bottle import Bottle, request
from bson.objectid import ObjectId

api_app = Bottle()


@api_app.post('/device')
def add_device(db):
    token = request.forms.get('token', None)
    if token:
        id = db['devices'].insert({'device': token})
        return {'id': str(id)}
    return {'error': '"token" is required.'}


@api_app.post('/push')
def send_push(db):
    device = request.forms.get('device', None)
    custom_payload = request.forms.get('payload', None)

    if device and custom_payload:
        device = db['devices'].find_one({'_id': ObjectId(device)})

        apns = APNs(use_sandbox=True,
                    cert_file='aps_voip.pem',
                    key_file='aps_voip_key.pem', enhanced=True)

        # Send a notification
        custom_payload = json.loads(custom_payload)
        payload = Payload(**custom_payload)
        identifier = random.getrandbits(32)

        apns.gateway_server.send_notification(device['device'], payload, identifier=identifier)

        def response_listener(error_response):
            print "client get error-response: " + str(error_response)

        apns.gateway_server.register_response_listener(response_listener)
    else:
        return {'error': '"device" and "payload" are required.'}

    return {'device': device, 'payload': custom_payload}
