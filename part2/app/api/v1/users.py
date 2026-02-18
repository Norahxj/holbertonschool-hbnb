from flask import jsonify, request
from models.user import User
from models import storage
from api.v1.views import app_views

@app_views.route("/users/", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON"}), 400

    required = ["first_name", "last_name", "email", "password"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    is_admin = data.get("is_admin", False)
    is_owner = data.get("is_owner", False)

    try:
        user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=data["password"],
            is_admin=is_admin,
            is_owner=is_owner
        )
        storage.new(user)
        storage.save()
        return jsonify(user.to_dict()), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app_views.route("/users/", methods=["GET"])
def get_users():
    all_users = storage.all("User")
    return jsonify([u.to_dict() for u in all_users.values()])


@app_views.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = storage.get("User", user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    all_users = storage.all("User")
    if not all_users:
        return jsonify({"error": "No users found"}), 404

    current_user = list(all_users.values())[0]

    if not current_user.is_admin:
        return jsonify({"error": "Admins only"}), 403

    user = storage.get("User", user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    storage.delete(user)
    storage.save()
    return jsonify({"message": "User deleted"})
