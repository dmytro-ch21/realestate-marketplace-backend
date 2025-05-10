from flask import Blueprint, request, jsonify
from app.services.listing_service import ListingService

listing_bp = Blueprint("listings", __name__)


@listing_bp.route("/listings", methods=["POST"])
def create_listing():
    # capture the data from request
    data = request.get_json()

    if not data:
        return jsonify(
            {
                "error": "400 Bad Request",
                "message": f"Data as JSON not provided"
            }
        ), 400

    if "owner_id" not in data or not data.get("owner_id"):
        return jsonify(
            {
                "error": "400 Bad Request",
                "message": f"Required field 'owner_id' is missing"
            }
        ), 400

    if "title" not in data or not data.get("title"):
        return jsonify(
            {
                "error": "400 Bad Request",
                "message": f"Required field 'title' is missing"
            }
        ), 400

    if "price" not in data or not data.get("price"):
        return jsonify(
            {
                "error": "400 Bad Request",
                "message": f"Required field 'price' is missing"
            }
        ), 400

    listing = ListingService.create_listing(
        owner_id=data.get("owner_id"),
        title=data.get("title"),
        price=data.get("price"),
        data=data
    )

    if listing:
        return jsonify({
                "message": "Successfully created a new listing", 
                "listing": listing.serialize()
            }), 201
    else: 
        return jsonify({
                "message": "Something went wrond while creating the listing"
            }), 400

@listing_bp.route("/listings", methods=["GET"])
def get_all_listings():
    listings = ListingService.get_all_listings()
    if listings:
        return jsonify([l.serialize() for l in listings])
    else:
        return jsonify({
            "message": "Seems like there is an issue"
        }), 404