"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
import json
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    # this is how you can use the Family datastructure by calling its methods

    # members = jackson_family.get_all_members()
    # response_body = {
    #     "family": members
    # }
    # return jsonify(response_body), 200
    response = jackson_family.get_all_members()
    if  response is None : 
      raise APIException("Record is not found", status_code=500)

    return jsonify({"family": response}), 200


@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):

    response = jackson_family.get_member(id)
    if response == None :
      raise APIException("Member not found", status_code=400)
    return jsonify({"family":response}), 200    

 

@app.route('/members', methods=['POST'])
def add_member():
    request_data=request.get_json()
    request_data["id"]=jackson_family._generateId()
    jackson_family.add_member(request_data)

    # member = request.data
    # text_data = json.loads(member)
    # jackson_family.add_member(text_data)

    # print({"family":jackson_family.get_all_members()})
    
    return jsonify({
        "message":"Member created sucessfully",
        "member":request_data
    }), 200    


@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    member=jackson_family.get_member(id)
    if member is None:
       raise APIException("invalid id", status_code=500) 
    jackson_family.delete_member(id)
    return jsonify({"family":jackson_family.get_all_members()}), 200    



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
