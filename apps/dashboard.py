from bottle import Bottle, template

app = Bottle()


@app.get('/login')
def login():
    return template('dashboard/login')
