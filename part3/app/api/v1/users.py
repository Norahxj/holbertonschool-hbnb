from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.services import facade
import re

api = Namespace('users', description='User operations')


def is_valid_email(email):
    pattern = r'^[^@]+@[^@]+\.[^@]+$'
    return re.match(pattern, email)


user_model = api.model('User', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'is_admin': fields.Boolean(required=False)
})


update_user_model = api.model('UpdateUser', {
    'first_name': fields.String(required=False),
    'last_name': fields.String(required=False),
    'email': fields.String(required=False),
    'password': fields.String(required=False),
    'is_admin': fields.Boolean(required=False)
})


@api.route('/')
class UserList(Resource):

    @jwt_required()
    @api.expect(user_model, validate=True)
    def post(self):
        """Admin only: create user"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload

        if not is_valid_email(user_data['email']):
            return {'error': 'Invalid email format'}, 400

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        user = facade.create_user(user_data)

        return {
            'id': user.id,
            'message': 'User registered successfully'
        }, 201

    def get(self):
        """Get all users"""
        users = facade.get_all_users()

        return [
            {
                'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email,
                'is_admin': u.is_admin
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
            'email': user.email,
            'is_admin': user.is_admin
        }, 200

    @jwt_required()
    @api.expect(update_user_model, validate=True)
    def put(self, user_id):
        """Update user"""
        claims = get_jwt()
        current_user = get_jwt_identity()
        data = api.payload or {}

        is_admin = claims.get('is_admin', False)

        if not is_admin and current_user != user_id:
            return {'error': 'Unauthorized action'}, 403

        if not is_admin and ('email' in data or 'password' in data):
            return {'error': 'You cannot modify email or password'}, 400

        if 'email' in data:
            if not is_valid_email(data['email']):
                return {'error': 'Invalid email format'}, 400

            existing_user = facade.get_user_by_email(data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        user = facade.update_user(user_id, data)

        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        }, 200
