from flask_socketio import emit, disconnect
from flask import request, current_app
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
        socketio.enter_room(request.sid, f"user_{user['id']}")
        send_all_notifications(user["id"])
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
        socketio.leave_room(request.sid, f"user_{user_elems['id']}")
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
        socketio.emit('response', {'data': f"Message reçu :"}, broadcast=True)
    except Exception as e:
        print("Erreur de décodage JSON :", e)
        socketio.emit('response', {'data': f"Erreur de décodage JSON : {e}"}, broadcast=True)

@socketio.on('my event')
def handle_my_event(data):
    print("Event reçu :", data)
    socketio.emit('response', {'data': f"Event reçu : {data}"}, broadcast=True)


def send_notification(emitter, receiver, action, message):
    try:
        db = get_db()
        print(f"Notification de {emitter} à {receiver} : {action} - {message}")
        user_emitter = None
        user_receiver = None
        with db.cursor() as cur:
            cur.execute('SELECT * FROM users WHERE id = %s', (emitter,))
            user_emitter = cur.fetchone()
            cur.execute('SELECT * FROM users WHERE id = %s', (receiver,))
            user_receiver = cur.fetchone()
            if user_receiver is None or user_emitter is None:
                return
            cur.execute('INSERT INTO waiting_notifications (emmiter, receiver, action, message) VALUES (%s, %s, %s, %s)', (emitter, receiver, action, message))
            db.commit()
            socketio.emit('notification', {'author_id':user_emitter["id"], 'author_name':f"{user_emitter['firstname']} {user_emitter['lastname']}", 'action':action, 'message':message}, room=f"user_{user_receiver['id']}")
    except Exception as e:
        print(f"Erreur d'envoi de notification : {e}")

def send_all_notifications(user_id):
    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM waiting_notifications WHERE receiver = %s', (user_id,))
        for notif in cur.fetchall():
            cur.execute('SELECT * FROM users WHERE id = %s', (notif["emmiter"],))
            user_emitter = cur.fetchone()
            if user_emitter is None:
                cursor.execute('DELETE FROM waiting_notifications WHERE id = %s', (notif["id"],))
                db.commit()
                continue
            socketio.emit('notification', {'author_id':user_emitter["id"], 'author_name':f"{user_emitter['firstname']} {user_emitter['lastname']}", 'action':notif["action"], 'message':notif["message"]}, room=f"user_{user_id}")

def delete_all_notifications(user_id):
    db = get_db()
    with db.cursor() as cur:
        cur.execute('DELETE FROM waiting_notifications WHERE receiver = %s', (user_id,))
        db.commit()