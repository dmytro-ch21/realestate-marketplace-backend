from flask import Blueprint, request, jsonify
from app.utils.validators import is_valid_email, is_valid_password, is_valid_username
from app.services.user_service import UserService

user_bp = Blueprint("users", __name__)

@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id: int):
    # have accessed the service layer to get one user
    user = UserService.get_user_by_id(user_id)
    if user:
        return jsonify(user.serialize())
    else:
        return jsonify(
            {
                "error": "404 Not Found",
                "message": f"User with id: {user_id} not found."
            }
        )


@user_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user_by_id(user_id: int):
    # need to get the user by id
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify(
            {
                "error": "404 Not Found",
                "message": f"User with id: {user_id} not found."
            }
        ), 404

    data = request.get_json()
    if not data:
        return jsonify(
            {
                "error": "400 Bad Request",
                "message": f"Data as JSON not provided"
            }
        ), 400

    # Manual validation
    if "email" in data and (not data.get("email") or not is_valid_email(data.get("email"))):
        return jsonify({"error": "email property fails validation"}), 400

    if "username" in data and (not data.get("username") or not is_valid_username(data.get("username"))):
        return jsonify({"error": "username property fails validation"}), 400

    if "password" in data and (not data.get("password") or not is_valid_password(data.get("password"))):
        return jsonify({"error": "password property fails validation"}), 400

    # once validation passed we update the record
    updated_user = UserService.update_user(user, **data)

    if updated_user:
        return jsonify({
            "message": "User Successfully updated",
            "user": updated_user.serialize()
        }), 200
    else:
        return jsonify({
            "message": "Something went wrong while updating the user information"
        }), 400

