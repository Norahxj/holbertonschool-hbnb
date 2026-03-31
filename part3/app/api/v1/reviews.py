from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True),
    'place_id': fields.String(required=True)
})

update_review_model = api.model('UpdateReview', {
    'text': fields.String(required=False),
    'rating': fields.Integer(required=False)
})


@api.route('/')
class ReviewList(Resource):

    def get(self):
        """Get all reviews"""
        reviews = facade.get_all_reviews()

        return [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating
            } for r in reviews
        ], 200

    @jwt_required()
    @api.expect(review_model, validate=True)
    def post(self):
        """Authenticated: create review"""
        review_data = api.payload
        current_user = get_jwt_identity()

        place = facade.get_place(review_data["place_id"])
        if not place:
            return {"error": "Place not found"}, 404

        if place.owner.id == current_user:
            return {"error": "You cannot review your own place"}, 400

        for review in facade.get_all_reviews():
            if review.user.id == current_user and review.place.id == review_data["place_id"]:
                return {"error": "You have already reviewed this place"}, 400

        review_data["user_id"] = current_user

        try:
            review = facade.create_review(review_data)
            return {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": review.user.id,
                "place_id": review.place.id
            }, 201
        except ValueError as e:
            return {"error": str(e)}, 400


@api.route('/<review_id>')
class ReviewResource(Resource):

    def get(self, review_id):
        """Get review by ID"""
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user.id,
            "place_id": review.place.id
        }, 200

    @jwt_required()
    @api.expect(update_review_model, validate=True)
    def put(self, review_id):
        """Owner or admin: update review"""
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        claims = get_jwt()
        current_user = get_jwt_identity()
        is_admin = claims.get('is_admin', False)

        if not is_admin and review.user.id != current_user:
            return {"error": "Unauthorized action"}, 403

        review_data = api.payload or {}

        try:
            updated_review = facade.update_review(review_id, review_data)

            if not updated_review:
                return {"error": "Review not found"}, 404

            return {
                "message": "Review updated successfully",
                "id": updated_review.id,
                "text": updated_review.text,
                "rating": updated_review.rating,
                "user_id": updated_review.user.id,
                "place_id": updated_review.place.id
            }, 200

        except ValueError as e:
            return {"error": str(e)}, 400

    @jwt_required()
    def delete(self, review_id):
        """Owner or admin: delete review"""
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        claims = get_jwt()
        current_user = get_jwt_identity()
        is_admin = claims.get('is_admin', False)

        if not is_admin and review.user.id != current_user:
            return {"error": "Unauthorized action"}, 403

        deleted = facade.delete_review(review_id)

        if not deleted:
            return {"error": "Review not found"}, 404

        return {"message": "Review deleted successfully"}, 200
