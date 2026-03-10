from flask_restx import Namespace, Resource, fields
from app.services import facade
import re

api = Namespace('users', description='User operations')


def is_valid_email(email):
    pattern = r'^[^@]+@[^@]+\.[^@]+'
    return re.match(pattern, email)


user_model = api.model('User', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True)
})


@api.route('/')
class UserList(Resource):

    @api.expect(user_model, validate=True)
    def post(self):
        """Create user"""

        user_data = api.payload

        if not is_valid_email(user_data['email']):
            return {'error': 'Invalid email format'}, 400

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        user = facade.create_user(user_data)

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 201


    def get(self):
        """Get all users"""

        users = facade.get_all_users()

        return [
            {
                'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email
            }
            for u in users
        ], 200


@api.route('/<user_id>')
class UserResource(Resource):

    def get(self, user_id):
        """Get user by ID"""

        user = facade.get_user(user_id)

        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200


    @api.expect(user_model)
    def put(self, user_id):
        """Update user"""

        data = api.payload

        if 'email' in data and not is_valid_email(data['email']):
            return {'error': 'Invalid email format'}, 400

        user = facade.update_user(user_id, data)

        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
