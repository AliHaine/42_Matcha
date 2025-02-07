from flask_socketio import emit
from . import socketio
import json

@socketio.on('connect')
def handle_connect():
    print("Un client est connecté")
    emit('message', {'data': 'Bienvenue !'})

@socketio.on('disconnect')
def handle_disconnect():
    print("Un client s'est déconnecté")

@socketio.on('message')
def handle_chat_message(data):
    print("Message reçu :", data, type(data))
    try:
        if type(data) == str:
            print("Message reçu (str) :", data, type(data))
            data = json.loads(data)
        print("Message reçu (décodé) :", data, type(data))
        emit('response', {'data': f"Message reçu :"}, broadcast=True)
    except Exception as e:
        print("Erreur de décodage JSON :", e)
        emit('response', {'data': f"Erreur de décodage JSON : {e}"}, broadcast=True)

@socketio.on('my event')
def handle_my_event(data):
    print("Event reçu :", data)
    emit('response', {'data': f"Event reçu : {data}"}, broadcast=True)
