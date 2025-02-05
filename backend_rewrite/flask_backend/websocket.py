from flask_socketio import emit
from . import socketio

@socketio.on('connect')
def handle_connect():
    print("Un client est connecté")
    emit('message', {'data': 'Bienvenue !'})

@socketio.on('disconnect')
def handle_disconnect():
    print("Un client s'est déconnecté")

@socketio.on('chat_message')
def handle_chat_message(data):
    print("Message reçu :", data)
    emit('response', {'data': f"Message reçu : {data}"}, broadcast=True)
