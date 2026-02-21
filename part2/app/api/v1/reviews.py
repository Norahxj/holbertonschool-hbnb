from flask import Flask, request, jsonify, abort
from Model.place import Place
from Model.review import Review
from Model.user import User


entity_type = "reviews"

def create_review_for_place(review_data, place_id):
    """Create a new review for a place"""
    data = review_data
    user_id = data.get('user_id')
    rating = data.get('rating')
    comment = data.get('comment')

    # Validate input
    if not (user_id and rating and comment):
        abort(400, 'Missing required fields')

    # Validate rating
    if rating not in range(1, 6):
        abort(400, 'Rating must be between 1 and 5')

    # Check if user and place exist
    if not data_manager.get('users', user_id):
        abort(404, f'User with ID {user_id} not found')
    if not data_manager.get('places', place_id):
        abort(404, f'Place with ID {place_id} not found')

    # Create review object
    review = Review(review_data.get("user_id"), place_id, review_data.get("comment"), review_data.get("rating"))

    # Save review
    data_manager.save('reviews', review.to_dict(), review.user_id, review.review_id)

    return jsonify(review.to_dict()), 201


def get_reviews_by_user(user_id):
    """Retrieve all reviews written by a specific user"""
    reviews = [review for review in data_manager.get('reviews').values() if review['user_id'] == user_id]
    if not reviews:
        abort(404, f'No reviews found for user ID {user_id}')

    return jsonify(reviews), 200

def get_reviews_for_place(place_id):
    """Retrieve reviews for a specific place."""
    # Check if place exists
    place = data_manager.get('places', place_id)
    if not place:
        abort(404, f'Place with ID {place_id} not found')

def get_review(review_id):
    review = data_manager.get('reviews', review_id)
    if not review:
        abort(404, f'Review with ID {review_id} not found')

    return jsonify(review), 200

def update_review(review_data, review_id):
    # Validate input
    user_id = review_data.get("user_id")
    rating = review_data.get("rating")
    comment = review_data.get("comment")
    
    if not (user_id and rating and comment):
        abort(400, 'Missing required fields')

    # Validate rating
    if rating not in range(1, 6):
        abort(400, 'Rating must be between 1 and 5')

    # Check if review exists
    review = data_manager.get('reviews', review_id)
    if not review:
        abort(404, f'Review with ID {review_id} not found')

    # Ensure user can not update other user's reviews
    # if review['user_id'] != user_id:
    #     abort(403, 'You are not allowed to update this review')

    # Update review object
    review['user_id'] = user_id
    review['rating'] = rating
    review['comment'] = comment
    review['updated_at'] = None

    # Save updated review
    data_manager.update('reviews', review, review_id)

    return jsonify(review), 200


def delete_review(self, review_id):
    """Delete a specific review"""
    review = data_manager.get('reviews', review_id)
    if not review:
        abort(404, f'Review with ID {review_id} not found')

    data_manager.delete('reviews', review_id)

    return '', 204
