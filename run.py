from bottle import run
from app import main

if __name__ == '__main__':
    run(main, host='localhost', port='8080', debug=True, reloader=True)
