from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')


amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):

    @api.expect(amenity_model)
    def post(self):
        """Register a new amenity"""

        amenity_data = api.payload

        if not amenity_data.get('name'):
            return {'error': 'Invalid input data'}, 400

        amenity = facade.create_amenity(amenity_data)

        return {
            'id': amenity.id,
            'name': amenity.name
        }, 201


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


    @api.expect(amenity_model)
    def put(self, amenity_id):
        """Update amenity"""

        data = api.payload

        if not data.get('name'):
            return {'error': 'Invalid input data'}, 400

        amenity = facade.update_amenity(amenity_id, data)

        if not amenity:
            return {'error': 'Amenity not found'}, 404

        return {'message': 'Amenity updated successfully'}, 200
