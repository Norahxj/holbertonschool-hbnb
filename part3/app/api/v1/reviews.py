from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True),
    'user_id': fields.String(required=True),
    'place_id': fields.String(required=True)
})

@api.route('/')
class ReviewList(Resource):

    @api.expect(review_model)
    def post(self):

        review_data = request.json

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


    def get(self):

        reviews = facade.get_all_reviews()

        return [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating
            } for r in reviews
        ], 200


@api.route('/<review_id>')
class ReviewResource(Resource):

    def get(self, review_id):

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


    def put(self, review_id):

        review_data = request.json

        try:
            review = facade.update_review(review_id, review_data)

            if not review:
                return {"error": "Review not found"}, 404

            return {"message": "Review updated successfully"}, 200

        except ValueError as e:
            return {"error": str(e)}, 400


    def delete(self, review_id):

        deleted = facade.delete_review(review_id)

        if not deleted:
            return {"error": "Review not found"}, 404

        return {"message": "Review deleted successfully"}, 200
