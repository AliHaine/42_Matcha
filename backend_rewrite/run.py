from flask_backend import create_app, socketio
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../settings/.flask.env'))

if __name__ == '__main__':
    try:
        app = create_app()
        socketio.run(app, host=os.getenv('HOSTNAME', default='127.0.0.1'), port=os.getenv("PORT", default=5000), debug=os.getenv("DEBUG", default='False') == 'True')
    except Exception as e:
        print(f"Error creating app: {e}")
        exit(1)