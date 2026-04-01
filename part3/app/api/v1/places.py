from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(description='ID of the owner'),
    'amenities': fields.List(fields.String, required=False, description='List of amenities IDs')
})


@api.route('/')
class PlaceList(Resource):
    def get(self):
        """Public: get all places"""
        places = facade.get_all_places()
        return [{
            "id": p.id,
            "title": p.title,
            "price": p.price,
            "latitude": p.latitude,
            "longitude": p.longitude,
            "owner_id": p.owner_id
        } for p in places], 200

    @jwt_required()
    @api.expect(place_model, validate=True)
    def post(self):
        """Authenticated: create place"""
        try:
            place_data = api.payload
            current_user = get_jwt_identity()
            place_data["owner_id"] = current_user

            new_place = facade.create_place(place_data)
            return {
                "id": new_place.id,
                "title": new_place.title,
                "description": new_place.description,
                "price": new_place.price,
                "latitude": new_place.latitude,
                "longitude": new_place.longitude,
                "owner_id": new_place.owner_id
            }, 201
        except ValueError as e:
            return {"error": str(e)}, 400


@api.route('/<place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        """Public: get place by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        owner = facade.get_user(place.owner_id)

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": {
                "id": owner.id,
                "first_name": owner.first_name,
                "last_name": owner.last_name,
                "email": owner.email
            } if owner else None,
            "amenities": []
        }, 200

    @jwt_required()
    @api.expect(place_model, validate=False)
    def put(self, place_id):
        """Owner or admin: update place"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        claims = get_jwt()
        current_user = get_jwt_identity()
        is_admin = claims.get('is_admin', False)

        if not is_admin and place.owner_id != current_user:
            return {"error": "Unauthorized action"}, 403

        place_data = api.payload or {}
        if "owner_id" in place_data and not is_admin:
            del place_data["owner_id"]

        try:
            updated_place = facade.update_place(place_id, place_data)
            if not updated_place:
                return {"error": "Place not found"}, 404

            return {
                "message": "Place updated successfully",
                "id": updated_place.id,
                "title": updated_place.title,
                "description": updated_place.description,
                "price": updated_place.price,
                "latitude": updated_place.latitude,
                "longitude": updated_place.longitude,
                "owner_id": updated_place.owner_id
            }, 200
        except ValueError as e:
            return {"error": str(e)}, 400


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    def get(self, place_id):
        """Public: get reviews by place"""
        reviews = facade.get_reviews_by_place(place_id)

        if reviews is None:
            return {"error": "Place not found"}, 404

        return [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
                "user_id": r.user_id,
                "place_id": r.place_id
            } for r in reviews
        ], 200
