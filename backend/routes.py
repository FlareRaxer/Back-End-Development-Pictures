from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """
    This endpoint will return all pictures in the data list
    """
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """
    This endpoint returns a single picture based on its id
    """
    picture = next((item for item in data if item["id"] == id), None)

    if picture is None:
        abort(404, "Picture not found")

    return jsonify(picture), 200


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """
    This endpoint will create a new picture from the posted data
    """
    new_picture = request.get_json()
    new_id = new_picture.get("id")

    if any(p["id"] == new_id for p in data):
        return jsonify({"Message": f"picture with id {new_id} already present"}), 302

    data.append(new_picture)

    return jsonify(new_picture), 201


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """
    This endpoint will update a picture based on the id
    """
    # Find the picture to update in the data list
    picture = next((p for p in data if p['id'] == id), None)
    
    # If the picture is not found, return a 404 error
    if not picture:
        abort(404)

    # Get the updated data from the request body
    updated_data = request.get_json()
    
    # Update the picture's dictionary with the new data
    picture.update(updated_data)

    # Return the updated picture with a 200 OK status
    return jsonify(picture), 200


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """
    This endpoint will delete a picture based on the id
    """
    # Find the picture to delete
    picture_to_delete = next((p for p in data if p['id'] == id), None)

    # If the picture is not found, return a 404 error with a message
    if not picture_to_delete:
        return jsonify({"message": "picture not found"}), 404

    # If the picture exists, remove it from the list
    data.remove(picture_to_delete)

    # Return a 204 No Content response, which indicates success
    return "", 204