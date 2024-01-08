from flask import Blueprint, request, jsonify
from database.database import Database 

auth_bp = Blueprint("auth", __name__)

database = Database()


# Sign up route
@auth_bp.route("/signup", methods=['POST'])
def signup():
    data = request.json
    success = database.auth.create(data['username'], data['email'], data['password'])
    return jsonify({'success': success}), (201 if success else 400)


# Login route
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user_id = database.auth.check_login(data['email'], data['password'])
    return jsonify({'user_id': user_id}), (200 if user_id != False else 401)

    
# User details route
@auth_bp.route("/details/<int:user_id>", methods=["GET"])
def user_details(user_id: int):
    user_data = database.auth.read(user_id)
    return jsonify(user_data) if user_data else ('', 404)


# Update user route
@auth_bp.route("/update/<int:user_id>", methods=["PUT"])
def update_user(user_id: int):
    data = request.json
    success = database.auth.update(user_id, data["new_username"], data["new_email"], data["new_password"])
    return jsonify({"success": success}), (200 if success else 400)


# Delete user route
@auth_bp.route("/delete/<int:user_id>", methods=['DELETE'])
def delete_user(user_id: int):
    success = database.auth.delete(user_id)
    return jsonify({"success": success}), (200 if success else 400)

