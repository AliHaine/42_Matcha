from flask import jsonify

def missing_token_callback(error):
    return jsonify({"success": False, "Error": "Please provide your token, or authenticate you to get one"})

def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"success": False, "Error": "Token expired. Please authenticate you to get a new one"})

def invalid_token_callback(error):
    return jsonify({"success": False, "Error": "Invalid token. Please authenticate you to get a new one"})

def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({"success": False, "Error": "Token revoked. Please authenticate you to get a new one"})
