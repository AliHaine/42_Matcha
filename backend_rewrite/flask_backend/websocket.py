from flask_socketio import emit, disconnect, join_room, leave_room
from flask import request, current_app
from . import socketio
from flask_jwt_extended import decode_token
from flask_jwt_extended.exceptions import (
    NoAuthorizationError, JWTDecodeError, InvalidHeaderError
)
from .auth import is_token_revoked
from .db import get_db
import json

connected_users = {}

@socketio.on('connect')
def handle_connect():
    token = request.args.get('access_token', None)
    verify, decoded_token = check_jwt_validity(token)
    if verify is False:
        print(f"Connexion refusée : {decoded_token}")
        disconnect()
        return
    if not token:
        print("Connexion refusée : Pas de token JWT")
        disconnect()
        return
    try:
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
            connected_users[request.sid]['available_chats'] = []
            connected_users[request.sid]['token'] = token
        print(f"Utilisateur {user_email} connecté via WebSocket")
        join_room(f"user_{user['id']}")
        update_available_chats(request.sid)
        send_all_notifications(user["id"])
    except Exception as e:
        print(f"Erreur lors de la connexion WebSocket : {e}")
        disconnect()

@socketio.on('disconnect')
def handle_disconnect():
    user_elems = connected_users.get(request.sid, None)
    if user_elems is None:
        print("Déconnexion refusée : Utilisateur non trouvé")
        return
    db = get_db()
    with db.cursor() as cur:
        cur.execute('''
            UPDATE users 
            SET active_connections = active_connections - 1, 
                status = CASE WHEN active_connections - 1 = 0 THEN FALSE ELSE status END 
            WHERE id = %s;
        ''', (user_elems["id"],))
        db.commit()
        leave_room(f"user_{user_elems['id']}")
        del connected_users[request.sid]
    print(f"Utilisateur {user_elems['id']} déconnecté via WebSocket")

@socketio.on('message')
def handle_chat_message(data):
    verify, error = check_jwt_validity(connected_users[request.sid]["token"])
    if verify is False:
        print(f"Deconnexion forcee de {connected_users[request.sid]['id']} : {error}")
        disconnect()
        return
    print("Message reçu :", data, type(data))
    try:
        if type(data) == str:
            print("Message reçu (str) :", data, type(data))
            data = json.loads(data)
        print("Message reçu (décodé) :", data, type(data))
        if "service" in data:
            if data["service"] == "notification":
                parse_service_notification(data)
                return
            elif data["service"] == "message":
                parse_service_message(data)
                return
    except Exception as e:
        print("Erreur de décodage JSON :", e)


def send_notification(emitter, receiver, action, message):
    if action == "match" or action == "unmatch":
        for sid ,user in connected_users.items():
            if user["id"] == emitter:
                update_available_chats()
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

def delete_all_notifications(user_id):
    db = get_db()
    with db.cursor() as cur:
        cur.execute('DELETE FROM waiting_notifications WHERE receiver = %s', (user_id,))
        db.commit()

def send_all_notifications(user_id):
    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM waiting_notifications WHERE receiver = %s', (user_id,))
        for notif in cur.fetchall():
            cur.execute('SELECT * FROM users WHERE id = %s', (notif["emmiter"],))
            user_emitter = cur.fetchone()
            if user_emitter is None:
                cur.execute('DELETE FROM waiting_notifications WHERE id = %s', (notif["id"],))
                db.commit()
                continue
            socketio.emit('notification', {'author_id':user_emitter["id"], 'author_name':f"{user_emitter['firstname']} {user_emitter['lastname']}", 'action':notif["action"], 'message':notif["message"]}, room=f"user_{user_id}")

def parse_service_notification(data):
    if not "action" in data:
        return
    if data["action"] == "clear":
        delete_all_notifications(connected_users[request.sid]["id"])
        return
    
def update_available_chats(sid):
    user_id = connected_users[sid]["id"]
    available_chats = []
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT uv1.viewed_id AS matched_user FROM user_views uv1 JOIN user_views uv2 ON uv1.viewer_id = uv2.viewed_id AND uv1.viewed_id = uv2.viewer_id WHERE uv1.liked = TRUE AND uv2.liked = TRUE AND uv1.viewer_id = %s", (user_id,))
        for row in cur.fetchall():
            available_chats.append(row["matched_user"])
    connected_users[sid]['available_chats'] = available_chats
    print(f"Utilisateur {user_id} : {available_chats}")
    if len(available_chats) > 0:
        socketio.emit('available_chats', {'users':available_chats}, room=f"user_{user_id}")


def parse_service_message(data):
    if not "receiver" in data or not "message" in data:
        return
    # send_notification(data["emitter"], data["receiver"], "message", data["message"])
    emmiter_informations = connected_users[request.sid]
    if data["receiver"] not in emmiter_informations["available_chats"]:
        return
    print("TEST RECEIVER")
    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM users WHERE id = %s', (emmiter_informations["id"],))
        user_emitter = cur.fetchone()
        cur.execute('SELECT * FROM users WHERE id = %s', (data["receiver"],))
        user_receiver = cur.fetchone()
        if user_receiver is None or user_emitter is None:
            return
        try:
            cur.execute('INSERT INTO messages (sender_id, receiver_id, message) VALUES (%s, %s, %s)', (emmiter_informations["id"], data["receiver"], data["message"]))
            db.commit()
        except Exception as e:
            print(f"Erreur d'insertion de message : {e}")
            socketio.emit('error', {'message':'Failed to send message'}, room=f"user_{emmiter_informations['id']}")
            return
        socketio.emit('message', {'author_id':emmiter_informations["id"], 'message':data["message"]}, room=f"user_{data['receiver']}")
        socketio.emit('message', {'author_id':emmiter_informations["id"], 'message':data["message"]}, room=f"user_{emmiter_informations['id']}")
    return


def check_jwt_validity(token):
    """
    Vérifie la validité d'un token JWT et sa révocation.
    Retourne (bool, dict ou str):
      - True + données du token si valide.
      - False + message d'erreur si invalide.
    """
    if not token:
        return False, "Token manquant"

    try:
        decoded_token = decode_token(token)

        # Vérifier l'expiration du token
        if "exp" in decoded_token:
            import datetime
            exp_timestamp = decoded_token["exp"]
            now_timestamp = datetime.datetime.utcnow().timestamp()
            if now_timestamp > exp_timestamp:
                return False, "Token expiré"

        # Vérifier si le token a été révoqué
        jti = decoded_token.get("jti")
        if is_token_revoked(jti):
            return False, "Token révoqué"

        return True, decoded_token  # Token valide
    except NoAuthorizationError:
        return False, "Autorisation manquante"
    except JWTDecodeError:
        return False, "Token invalide"
    except InvalidHeaderError:
        return False, "Header JWT invalide"
    except Exception as e:
        return False, f"Erreur inconnue : {str(e)}"
