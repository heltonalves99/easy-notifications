import json
from apns import APNs, Payload
from bottle import Bottle, run, request
from bottle.ext.mongo import MongoPlugin
from bson.objectid import ObjectId

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


@app.post('/api/push')
def send_push(db):
    device = request.forms.get('device', None)
    custom_payload = request.forms.get('payload', None)

    if device and custom_payload:
        device = db['devices'].find_one({'_id': ObjectId(device)})

        apns = APNs(use_sandbox=False,
                    cert_file='aps_production.pem',
                    key_file='aps_production_key.pem')

        # Send a notification
        custom_payload = json.loads(custom_payload)
        payload = Payload(**custom_payload)
        apns.gateway_server.send_notification(device['device'], payload)
    else:
        return {'error': '"device" and "payload" are required.'}

    return {'device': device, 'payload': custom_payload}

run(app, host='localhost', port='8080', debug=True, reloader=True)
