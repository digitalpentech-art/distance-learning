from app import create_app
from extensions import socketio
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    socketio.run(app, debug=True)
