from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace('amenities', description='Amenity operations')


amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):

    def get(self):
        """Retrieve all amenities"""
        amenities = facade.get_all_amenities()

        return [
            {
                'id': a.id,
                'name': a.name
            }
            for a in amenities
        ], 200

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    def post(self):
        """Admin only: register a new amenity"""
        claims = get_jwt()

        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = api.payload

        if not amenity_data.get('name'):
            return {'error': 'Invalid input data'}, 400

        amenity = facade.create_amenity(amenity_data)

        return {
            'id': amenity.id,
            'name': amenity.name
        }, 201


@api.route('/<amenity_id>')
class AmenityResource(Resource):

    def get(self, amenity_id):
        """Get amenity by ID"""
        amenity = facade.get_amenity(amenity_id)

        if not amenity:
            return {'error': 'Amenity not found'}, 404

        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    def put(self, amenity_id):
        """Admin only: update amenity"""
        claims = get_jwt()

        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        data = api.payload

        if not data.get('name'):
            return {'error': 'Invalid input data'}, 400

        amenity = facade.update_amenity(amenity_id, data)

        if not amenity:
            return {'error': 'Amenity not found'}, 404

        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200
