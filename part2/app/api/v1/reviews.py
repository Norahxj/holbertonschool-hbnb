from flask_restx import Namespace, Resource, fields
from app.persistence.repository import storage
from app.models.review import Review

api = Namespace("reviews", description="Reviews operations")

review_model = api.model("Review", {
    "id": fields.String(readonly=True),
    "user_id": fields.String(required=True),
    "place_id": fields.String(required=True),
    "comment": fields.String(required=True),
    "rating": fields.Integer(required=True, min=1, max=5)
})

@api.route("/")
class ReviewList(Resource):
    @api.marshal_list_with(review_model)
    def get(self):
        return storage.all_reviews()

    @api.expect(review_model)
    @api.marshal_with(review_model, code=201)
    def post(self):
        data = api.payload

        # validation
        if not storage.get_user(data["user_id"]):
            api.abort(404, "User not found")

        if not storage.get_place(data["place_id"]):
            api.abort(404, "Place not found")

        review = Review(
            user_id=data["user_id"],
            place_id=data["place_id"],
            comment=data["comment"],
            rating=data["rating"]
        )

        storage.save_review(review)
        return review, 201


@api.route("/<string:review_id>")
class ReviewItem(Resource):
    @api.marshal_with(review_model)
    def get(self, review_id):
        review = storage.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return review

    def delete(self, review_id):
        review = storage.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        storage.delete_review(review_id)
        return "", 204
