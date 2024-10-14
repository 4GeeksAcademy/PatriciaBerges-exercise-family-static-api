"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

def new_member(name, age, numbers):
    return {
        "first_name": name,
        "last_name": jackson_family.last_name,
        "age": age,
        "lucky_numbers": numbers
    }

jackson_family.add_member(new_member("John", 33, [7, 13, 22]))
jackson_family.add_member(new_member("Jane", 35, [10, 14, 3]))
jackson_family.add_member(new_member("Jimmy", 5, [1,]))

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    members_data = list(map(lambda person: {"id": person['id'], "first_name": person['first_name']}, members))
    response_body = {
        "Family members": members_data
    }
    return jsonify(response_body), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_single_member(member_id):
    member = jackson_family.get_member(member_id)
    response_body = {
        "id": member['id'],
        "first_name": member['first_name'],
        "age": member['age'],
        "lucky_numbers": member['lucky_numbers']
    }
    return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def handle_post_member(member):
    if member['first_name'] not in member:
        return ("New member must have a first_name"), 400
    elif member['age'] not in member:
        return ("New member must have age"), 400
    elif member['lucky_numbers'] not in member:
        return ("New member must have lucky_numbers"), 400
    else:
        jackson_family.add_member(member)
        response_body = jackson_family.get_all_members()
        return jsonify(response_body), 200
    
@app.route('/member/<int:member_id>', methods=['DELETE'])
def handle_delete(member_id):
    jackson_family.delete_member(member_id)
    response_body = jackson_family.get_all_members()
    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
