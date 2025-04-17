def parse_post_actions(user, user_getting, action):
    """
    Parse the action of a post and update the database accordingly.
    """
    from flask import current_app, jsonify
    from .db import get_db
    from .websocket import send_notification
    from .profiles_utils import get_user_view
    db = get_db()
    try:
        with db.cursor() as cursor:
            user_view = get_user_view(user_getting["id"], user["id"])
            old_matched = cursor.execute(current_app.config["QUERIES"].get("-- check match"), {"user_id_1": user['id'], "user_id_2": user_getting['id']})
            if old_matched is None:
                old_matched = False
            else:
                old_matched = True
            success = False
            message = ""
            if action == 'like':
                success, message = like_action(user, user_getting, user_view, old_matched)
            elif action == 'block':
                success = block_action(user, user_getting, user_view)
            elif action == 'report':
                cursor.execute("UPDATE user_views SET reported = TRUE WHERE id = %s", (user_view["id"],))
                db.commit()
            else:
                message = "Invalid action"
            if success:
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'error': message})
    except Exception as e:
        current_app.logger.error(f"Error in parse_post_actions: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'})
        
def like_action(user, user_getting, user_view, old_matched):
    """
    Like action for a post.
    """
    from .websocket import send_notification
    from flask import jsonify, current_app
    from .db import get_db
    db = get_db()
    with db.cursor() as cursor:
        if user_view["blocked"]:
            return False, "User is blocked"
        if user_getting["pictures_number"] == 0:
            return False, "User has no profile picture set"
        cursor.execute("UPDATE user_views SET liked = NOT liked WHERE id = %s", (user_view["id"],))
        db.commit()
        cursor.execute(current_app.config["QUERIES"].get("-- check match"), {"user_id_1": user['id'], "user_id_2": user_getting['id']})
        actual_match = cursor.fetchone()
        if actual_match is not None:
            actual_match = True
        else:
            actual_match = False
        if old_matched == False and actual_match == True:
            send_notification(user["id"], user_getting["id"], "match", "User matched with you")
            send_notification(user_getting["id"], user["id"], "match", "User matched with you")
        elif old_matched == True and actual_match == False:
            send_notification(user["id"], user_getting["id"], "unmatch", "User unmatched with you")
            send_notification(user_getting["id"], user["id"], "unmatch", "User unmatched with you")
    return True, "Success"

def block_action(user, user_getting, user_view):
    """
    Block action for a post.
    """
    from .websocket import send_notification
    from flask import jsonify
    from .db import get_db
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("UPDATE user_views SET blocked = NOT blocked WHERE id = %s", (user_view["id"],))
        db.commit()
        if user_view["blocked"] == True:
            send_notification(user_getting["id"], user["id"], "unblock", "User unblocked you")
        else:
            cursor.execute("UPDATE user_views SET liked = FALSE WHERE id = %s", (user_view["id"],))
            send_notification(user_getting["id"], user["id"], "block", "User blocked you")
    return True