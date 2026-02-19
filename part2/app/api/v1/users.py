from flask_restx import Namespace, Resource, fields
from app.models.user import User
from app.persistence.repository import storage

api = Namespace("users", description="Users operations")

user_model = api.model("User", {
    "id": fields.String(readonly=True),
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True),
    "is_admin": fields.Boolean(default=False),
    "is_owner": fields.Boolean(default=False)
})


@api.route("/")
class UsersList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        return [u.to_dict() for u in storage.all_users()]

    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        data = api.payload

        user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=data["password"],
            is_admin=data.get("is_admin", False),
            is_owner=data.get("is_owner", False)
        )

        storage.save_user(user)
        return user.to_dict(), 201


@api.route("/<user_id>")
class UserItem(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        user = storage.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user.to_dict()

    def delete(self, user_id):
        users = storage.all_users()
        if not users:
            api.abort(404, "No users found")

        current_user = users[0]

        if not current_user.is_admin:
            api.abort(403, "Admins only")

        deleted = storage.delete_user(user_id)
        if not deleted:
            api.abort(404, "User not found")

        return {"message": "User deleted"}
