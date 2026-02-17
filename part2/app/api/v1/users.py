from flask_restx import Namespace, Resource, fields
from app.services.facade import Facade

api = Namespace("users", description="User operations")
facade = Facade()

user_model = api.model("User", {
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True),
    "is_admin": fields.Boolean(default=False),
    "is_owner": fields.Boolean(default=False),
})

@api.route("/")
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        return [u.to_dict() for u in facade.get_all_users()]

    @api.expect(user_model)
    @api.marshal_with(user_model)
    def post(self):
        return facade.create_user(api.payload).to_dict()


@api.route("/<string:user_id>")
class UserItem(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user.to_dict()

    @api.expect(user_model)
    @api.marshal_with(user_model)
    def put(self, user_id):
        user = facade.update_user(user_id, api.payload)
        if not user:
            api.abort(404, "User not found")
        return user.to_dict()

    def delete(self, user_id):
        deleted = facade.delete_user(user_id)
        if not deleted:
            api.abort(404, "User not found")
        return {"message": "User deleted"}
