from flask_backend import create_app, socketio
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../settings/.flask.env'))
app = create_app()

if __name__ == '__main__':
    socketio.run(app, host=os.getenv('HOSTNAME', default='127.0.0.1'), port=os.getenv("PORT", default=5000), debug=True)