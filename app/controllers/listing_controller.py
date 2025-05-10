from flask import Blueprint, request, jsonify
from app.services.listing_service import ListingService
import cloudinary.uploader

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


@listing_bp.route("/listings/<int:listing_id>", methods=["GET"])
def get_listing_by_id(listing_id: int):
    listing = ListingService.get_listings_by_id(listing_id)
    if listing:
        return jsonify(listing.serialize()), 200
    else:
        return jsonify({"error": f"Listing with id {listing_id} not found"}), 404


@listing_bp.route("/listings/owner/<int:owner_id>", methods=["GET"])
def get_listings_by_owner_id(owner_id: int):
    listings = ListingService.get_listings_by_owner_id(owner_id)
    if listings:
        return jsonify([l.serialize() for l in listings]), 200
    else:
        return jsonify({"error": f"Listings not found for given owner(user) id {owner_id}"}), 404


@listing_bp.route("/listings/<int:listing_id>", methods=["PUT"])
def update_listing(listing_id: int):
    # capture the data from request
    data = request.get_json()

    if not data:
        return jsonify(
            {
                "error": "400 Bad Request",
                "message": f"Data as JSON not provided"
            }
        ), 400

    if "owner_id" in data:
        return jsonify(
            {
                "error": "400 Bad Request",
                "message": f"Not allowed to change the owner id."
            }
        ), 400

    try:
        listing = ListingService.update_listing_by_id(
            listing_id=listing_id, **data)
        return jsonify({
            "message": "Successfully created a new listing",
            "listing": listing.serialize()
        }), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 404

@listing_bp.route("/listings/<int:listing_id>", methods=["DELETE"])
def delete_listing(listing_id: int):
    try:
        success = ListingService.delete_listing_by_id(listing_id)
        if success:
            return jsonify({"message": f"Listing with id {listing_id} successfully deleted"}) 
        else:
            return jsonify({"error": f"Listing with id {listing_id} failed to be deleted"}) 
    except ValueError as e:
        return jsonify({"error": "No Found", "message": str(e)})
    
@listing_bp.route("/listings/<int:listing_id>/images", methods=["POST"])
def upload_image(listing_id: int):
    listing = ListingService.get_listings_by_id(listing_id)

    if not listing:
        return jsonify({"error": f"Listing with id {listing_id} Not Found"}), 404

    if not request.content_type.startswith("multipart/form-data"):
        return jsonify({"error": "Content type should be multipart/form-data"})

    if "image" not in request.files:
        return jsonify({"error": "Image not provided"}), 400

    image_file = request.files.get("image")
    is_primary = request.form.get("is_primary", "")
    caption = request.form.get("caption", "")
    
    # upload image to claudinary
    upload_result = cloudinary.uploader.upload(
        image_file,
        folder="listing_images"
    )
    print('upload_result', upload_result)    
    # create a new listing image object
    
    listing_image = ListingService.add_listing_image(
        listing_id=listing_id,
        image_url=upload_result.get("secure_url"),
        claudinary_public_id=upload_result.get("public_id"),
        is_primary= True if is_primary.lower() == "true" else False,
        caption=caption
    )
    
    if listing_image:
        return jsonify(listing_image.serialize()), 201 
    else:
        return jsonify({"error": "Could not upload the image due to not existing listing"}), 404


    
    
    