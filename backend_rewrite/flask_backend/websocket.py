from datetime import datetime, timedelta
import sys
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
        disconnect()
        return
    if not token:
        disconnect()
        return
    try:
        user_email = decoded_token['sub']
        db = get_db()
        with db.cursor() as cur:
            cur.execute('SELECT * FROM users WHERE email = %s', (user_email,))
            user = cur.fetchone()
            if user is None:
                disconnect()
                return
            from .user import check_registration_status
            if check_registration_status(user["email"]) is False:
                disconnect()
                return
            cur.execute('UPDATE users SET status = TRUE, active_connections = active_connections + 1 WHERE email = %s', (user_email,))
            db.commit()
            connected_users[request.sid] = {}
            connected_users[request.sid]['id'] = user['id']
            connected_users[request.sid]['available_chats'] = []
            connected_users[request.sid]['token'] = token
        join_room(f"user_{user['id']}")
        update_available_chats(request.sid)
        send_all_notifications(user["id"])
    except Exception as e:
        disconnect()

@socketio.on('disconnect')
def handle_disconnect():
    user_elems = connected_users.get(request.sid, None)
    if user_elems is None:
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

@socketio.on('message')
def handle_chat_message(data):
    verify, error = check_jwt_validity(connected_users[request.sid]["token"])
    if verify is False:
        disconnect()
        return
    try:
        if type(data) == str:
            data = json.loads(data)
        if "service" in data:
            if data["service"] == "notification":
                parse_service_notification(data)
            elif data["service"] == "message":
                parse_service_message(data)
            sys.stdout.flush()
    except Exception as e:
        print("Erreur de décodage JSON :", e)


def send_notification(emitter, receiver, action, message):
    if action == "match" or action == "unmatch":
        sids_to_update = [sid for sid, user in connected_users.items() if user["id"] == emitter]
        for sid in sids_to_update:
            update_available_chats(sid)
    try:
        db = get_db()
        user_emitter = None
        user_receiver = None
        with db.cursor() as cur:
            cur.execute('SELECT * FROM users WHERE id = %s', (emitter,))
            user_emitter = cur.fetchone()
            cur.execute('SELECT * FROM users WHERE id = %s', (receiver,))
            user_receiver = cur.fetchone()
            if user_receiver is None or user_emitter is None:
                return
            blocked, message = check_id_blocked(emitter, receiver)
            if blocked:
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
    socketio.emit('available_chats', {'users':available_chats}, room=f"user_{user_id}")


def parse_service_message(data):
    if not "receiver" in data or not "message" in data:
        return
    emmiter_informations = connected_users[request.sid]
    if data["receiver"] not in emmiter_informations["available_chats"]:
        return
    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM users WHERE id = %s', (emmiter_informations["id"],))
        user_emitter = cur.fetchone()
        cur.execute('SELECT * FROM users WHERE id = %s', (data["receiver"],))
        user_receiver = cur.fetchone()
        if user_receiver is None or user_emitter is None:
            return
        blocked, message = check_id_blocked(emmiter_informations["id"], data["receiver"])
        if blocked:
            socketio.emit('error', {'message':message}, room=f"user_{emmiter_informations['id']}")
            print(f"Erreur d'envoi de message : {message}")
            return
        import re
        if re.match(r'^\s*$', data["message"]):
            return
        try:
            sanitized_message = data["message"]
            cur.execute('INSERT INTO messages (sender_id, receiver_id, message, type) VALUES (%s, %s, %s, %s)', (emmiter_informations["id"], data["receiver"], sanitized_message, "text"))
            db.commit()
            send_message({"message":data["message"], "type":"text", "author_id":emmiter_informations["id"], "created_at":datetime.now().strftime("%H:%M")}, rooms=[f"user_{data['receiver']}", f"user_{emmiter_informations['id']}"]) 
        except Exception as e:
            socketio.emit('error', {'message':'Failed to send message'}, room=f"user_{emmiter_informations['id']}")
            return
    return

def send_message(arguments={}, rooms=[]):
    db = get_db()
    cur = db.cursor()
    if len(arguments) == 0:
        return
    if len(rooms) == 0:
        return
    if "message" not in arguments or "type" not in arguments or "author_id" not in arguments or "created_at" not in arguments:
        return
    for room in rooms:
        try:
            socketio.emit('message', arguments, room=room)
            receiver = int(room.split("_")[-1])
            if receiver != arguments["author_id"]:
                cur.execute("SELECT created_at FROM messages WHERE (sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s) ORDER BY created_at DESC LIMIT 2", (arguments["author_id"], receiver, receiver, arguments["author_id"]))
                messages = cur.fetchall()
                if len(messages) == 2:
                    time_required = timedelta(seconds=300)
                    if messages[0]["created_at"] - messages[1]["created_at"] > time_required:
                        send_notification(arguments["author_id"], receiver, "chat", f"Vous avez un nouveau message de {arguments['author_id']}")
        except Exception as e:
            print(f"Erreur d'envoi de message : {e}")


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

def check_id_blocked(actual_id, target_id):
    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM user_views WHERE (viewer_id = %s AND viewed_id = %s AND blocked = TRUE) OR (viewer_id = %s AND viewed_id = %s AND blocked = TRUE)', (actual_id, target_id, target_id, actual_id))
        resp = cur.fetchone()
        if resp is not None:
            message = "Cet utilisateur vous a bloqué"
            if actual_id == resp["viewer_id"]:
                message = "Vous avez bloqué cet utilisateur"
            return True, message
    return False, ""
