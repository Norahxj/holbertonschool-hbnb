from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("users", description="User operations")

user_model = api.model("User", {
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True)
})

@api.route("/")
class UserList(Resource):

    @api.expect(user_model)
    def post(self):
        user = facade.create_user(api.payload)
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }, 201

    def get(self):
        users = facade.get_all_users()
        return [
            {
                "id": u.id,
                "first_name": u.first_name,
                "last_name": u.last_name,
                "email": u.email
            } for u in users
        ], 200


@api.route("/<user_id>")
class UserResource(Resource):

    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }, 200

    def put(self, user_id):
        user = facade.update_user(user_id, api.payload)
        if not user:
            return {"error": "User not found"}, 404
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }, 200
