from flask_restx import Namespace, Resource, fields
from app.models.place import Place
from app.persistence.repository import storage

api = Namespace("places", description="Places operations")

place_model = api.model("Place", {
    "id": fields.String(readonly=True),
    "title": fields.String(required=True),
    "description": fields.String(default=""),
    "price": fields.Float(default=0.0),
    "latitude": fields.Float(default=0.0),
    "longitude": fields.Float(default=0.0),
    "owner": fields.String(default=None)
})


@api.route("/")
class PlacesList(Resource):
    @api.marshal_list_with(place_model)
    def get(self):
        return [p.to_dict() for p in storage.all_places()]

    @api.expect(place_model)
    @api.marshal_with(place_model, code=201)
    def post(self):
        data = api.payload

        place = Place(
            title=data["title"],
            description=data.get("description", ""),
            price=data.get("price", 0.0),
            latitude=data.get("latitude", 0.0),
            longitude=data.get("longitude", 0.0),
            owner=data.get("owner", None)
        )

        storage.save_place(place)
        return place.to_dict(), 201


@api.route("/<place_id>")
class PlaceItem(Resource):
    @api.marshal_with(place_model)
    def get(self, place_id):
        place = storage.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        return place.to_dict()

    def delete(self, place_id):
        deleted = storage.delete_place(place_id)
        if not deleted:
            api.abort(404, "Place not found")
        return {"message": "Place deleted"}
