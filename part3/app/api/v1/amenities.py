from flask_restx import Namespace, Resource, fields
from app.models.amenity import Amenity
from app.persistence.repository import storage

api = Namespace("amenities", description="Amenities operations")

amenity_model = api.model("Amenity", {
    "id": fields.String(readonly=True),
    "name": fields.String(required=True),
    "description": fields.String(default="")
})


@api.route("/")
class AmenitiesList(Resource):
    @api.marshal_list_with(amenity_model)
    def get(self):
        return [a.to_dict() for a in storage.all_amenities()]

    @api.expect(amenity_model)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        data = api.payload

        amenity = Amenity(
            name=data["name"],
            description=data.get("description", "")
        )

        storage.save_amenity(amenity)
        return amenity.to_dict(), 201


@api.route("/<amenity_id>")
class AmenityItem(Resource):
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        amenity = storage.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity.to_dict()

    def delete(self, amenity_id):
        deleted = storage.delete_amenity(amenity_id)
        if not deleted:
            api.abort(404, "Amenity not found")
        return {"message": "Amenity deleted"}
