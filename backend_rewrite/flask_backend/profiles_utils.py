def get_user_view(viewer_id, viewed_id, accessed=False):
    """
    Get the user view from the database. If it doesn't exist, create it.
    If accessed is True, update the last_view and accessed fields.
    """
    from .db import get_db
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM user_views WHERE viewer_id = %s AND viewed_id = %s", (viewer_id, viewed_id,))
        user_view = cursor.fetchone()
        if user_view is None:
            cursor.execute("INSERT INTO user_views (viewer_id, viewed_id) VALUES (%s, %s)", (viewer_id, viewed_id,))
            db.commit()
            cursor.execute("SELECT * FROM user_views WHERE viewer_id = %s AND viewed_id = %s", (viewer_id, viewed_id,))
            user_view = cursor.fetchone()
        if accessed == True:
            cursor.execute("UPDATE user_views SET accessed = TRUE, last_view = NOW() WHERE viewer_id = %s AND viewed_id = %s", (viewer_id, viewed_id,))
            db.commit()
        return user_view
    
def parse_profile_type(user, user_getting):
    """
    parse the profile type of user that is getting viewed and return it
    """
    from flask import request, jsonify
    from .websocket import send_notification
    get_user_view(user_getting["id"], user["id"], accessed=True)
    if 'chat' in request.args and request.args['chat'] != 'true':
        send_notification(user_getting["id"], user["id"], "view", "User viewed your profile")
    if 'chat' in request.args and request.args['chat'] == 'true':
        if 'all_messages' in request.args and request.args['all_messages'] == 'true':
            return jsonify({'success': True, 'user': convert_to_chat_profile(user, user_getting, all_messages=True), 'chat': True})
        return jsonify({'success': True, 'user': convert_to_chat_profile(user, user_getting), 'chat': True})
    return jsonify({'success': True, 'user': convert_to_public_profile(user, user_getting)})


def convert_to_public_profile(user, user_requesting=None):
    """
    Convert a user to a public profile format.
    """
    from .db import get_db
    from flask import current_app
    cityID = user['city_id']
    city = ""
    db = get_db()
    if cityID is not None:
        with db.cursor() as cursor:
            cursor.execute("SELECT cityname, citycode FROM cities WHERE id = %s", (cityID,))
            cityElement = cursor.fetchone()
            city = cityElement['cityname'] + f" ({cityElement['citycode']})"
    lookingFor = [user['searching'], user['commitment'], user['frequency']]
    shape = [user['weight'], user['size'], user['shape']]
    health = [user['smoking'], user['alcohol'], user['diet']]
    interests = []
    matching = "none"
    with db.cursor() as cursor:
        # getting all interests
        cursor.execute(current_app.config['QUERIES'].get("-- get user interests"), {"user_id": user['id']})
        interests.extend(interest['name'] for interest in cursor.fetchall() or [])
        matching = "none"  # Valeur par défaut
        score = 0
        if user_requesting:
            if "score" in user:
                score = user["score"]
            else:
                from .matcha import calcul_score
                score = calcul_score(user_requesting, user)
            # Vérifie si l'utilisateur demandeur a déjà vu l'autre
            cursor.execute("""
                SELECT * FROM user_views 
                WHERE viewer_id = %s AND viewed_id = %s
            """, (user_requesting['id'], user['id']))
            user_view = cursor.fetchone()
            if user_view:
                if user_view["blocked"]:
                    matching = "block"
                elif user_view["liked"]:
                    matching = "like"
                    # Vérifie la réciprocité du like
                    cursor.execute(current_app.config["QUERIES"].get("-- check match"), {"user_id_1": user['id'], "user_id_2": user_requesting['id']})
                    user_viewed = cursor.fetchone()
                    if user_viewed:
                        matching = "match"
    base = {
        'id': user['id'],
        'firstname': user['firstname'],
        'lastname': user['lastname'],
        'username': user['username'],
        'age': user['age'],
        'city': city,
        'gender': user['gender'],
        'description': user['description'],
        'hetero': user['hetero'],
        'lookingFor': lookingFor,
        'shape': shape,
        'health': health,
        'interests': interests,
        'picturesNumber': user['pictures_number'],
        'status': user['status'],
        'fame_rate': user['fame_rate'],
        "matching": matching,
        "email_verified": user['email_verified'],
        "premium": user['premium'],
        "score": score,
        "last_connection": user['last_conn'].strftime("%Y-%m-%d %H:%M:%S") if user['active_connections'] == 0 else "Active",
    }
    return base

def convert_to_chat_profile(user, user_getting, all_messages=False):
    """
    Convert a user to a chat profile format.
    """
    from .db import get_db
    from flask import current_app
    cityID = user['city_id']
    city = ""
    db = get_db()
    if cityID is not None:
        with db.cursor() as cursor:
            cursor.execute("SELECT cityname FROM cities WHERE id = %s", (cityID,))
            cityElement = cursor.fetchone()
            city = cityElement['cityname']
    base_return = {
        'id': user['id'],
        'firstname': user['firstname'],
        'age': user['age'],
        'city': city,
        'picturesNumber': user['pictures_number'],
        'status': user['status'],
    }
    with db.cursor() as cursor:
        if all_messages == True:
            cursor.execute(current_app.config['QUERIES'].get("-- get chat messages ASC"), {'user_id_1': user['id'], 'user_id_2': user_getting['id'], "nb_messages": 500})
            allMessages = cursor.fetchall()
            if allMessages:
                messages = []
                for message in allMessages:
                    messages.append({
                        'message': message['message'],
                        'created_at': message['created_at'].strftime("%H:%M"),
                        'author_id': message['sender_id'],
                        'type': message['type'],
                    })
                base_return.update({
                    'allMessages': messages,
                })
        else:
            cursor.execute(current_app.config['QUERIES'].get("-- get chat messages DESC"), {'user_id_1': user['id'], 'user_id_2': user_getting['id'], "nb_messages": 1})
            lastMessage = cursor.fetchall()
            if lastMessage:
                message = {
                    'message': lastMessage[0]['message'],
                    'created_at': lastMessage[0]['created_at'].strftime("%H:%M"),
                    'author_id': lastMessage[0]['sender_id'],
                    'type': lastMessage[0]['type'],
                }
                base_return.update({
                    'lastMessage': message,
                })
        return base_return