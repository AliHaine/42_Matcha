from flask_socketio import emit, disconnect
from flask import request
from . import socketio
from flask_jwt_extended import decode_token
from .db import get_db
import json

@socketio.on('connect')
def handle_connect():
    token = request.args.get('access_token', None)
    if not token:
        print("Connexion refusée : Pas de token JWT")
        disconnect()
        return

    try:
        decoded_token = decode_token(token)
        user_email = decoded_token['sub']
        db = get_db()
        with db.cursor() as cur:
            cur.execute('SELECT * FROM users WHERE email = %s', (user_email,))
            user = cur.fetchone()
            if user is None:
                print("Connexion refusée : Utilisateur non trouvé")
                disconnect()
                return
        print(f"Utilisateur {user_email} connecté via WebSocket")
    except Exception as e:
        print(f"Erreur de décodage du JWT : {e}")
        disconnect()

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
