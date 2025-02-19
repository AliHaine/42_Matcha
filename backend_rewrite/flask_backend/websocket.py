from flask_socketio import emit, disconnect
from flask import request
from . import socketio
from flask_jwt_extended import decode_token
from .db import get_db
import json

connected_users = {}

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
            cur.execute('UPDATE users SET status = TRUE, active_connections = active_connections + 1 WHERE email = %s', (user_email,))
            db.commit()
            connected_users[request.sid] = {}
            connected_users[request.sid]['id'] = user['id']
        print(f"Utilisateur {user_email} connecté via WebSocket")
        available_chats = []
        with db.cursor() as cur:
            cur.execute("SELECT uv1.viewed_id AS matched_user FROM user_views uv1 JOIN user_views uv2 ON uv1.viewer_id = uv2.viewed_id AND uv1.viewed_id = uv2.viewer_id WHERE uv1.liked = TRUE AND uv2.liked = TRUE AND uv1.viewer_id = %s", (user["id"],))
            for row in cur.fetchall():
                available_chats.append(row["user2"])
        connected_users[request.sid]['available_chats'] = available_chats
        emit('init', {'data': f"Connecté en tant que {user_email}", 'available_chats':available_chats})
    except Exception as e:
        print(f"Erreur de décodage du JWT : {e}")
        disconnect()

@socketio.on('disconnect')
def handle_disconnect():
    user_elems = connected_users.get(request.sid, None)
    if user_elems is None:
        print("Déconnexion refusée : Utilisateur non trouvé")
        return
    db = get_db()
    with db.cursor() as cur:
        cur.execute('UPDATE users SET active_connections = active_connections - 1 WHERE id = %s', (user_elems["id"],))
        cur.execute('UPDATE users SET status = FALSE WHERE active_connections = 0 AND id = %s', (user_elems["id"],))
        db.commit()
        del connected_users[request.sid]
    print(f"Utilisateur {user_elems['id']} déconnecté via WebSocket")

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
