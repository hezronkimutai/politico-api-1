from flask import jsonify, request, abort, make_response
from ...v1 import version_1 as v1
from ..schemas.political_party_schema import PoliticalPartySchema
from ..models.political_party_model import PoliticalParty
from flask_jwt_extended import (jwt_required, get_jwt_identity)

db = PoliticalParty()

@v1.route('/parties', methods=['POST'])
@jwt_required
def create_political_party():
  """
    Endpoint for creating a political party
  """
  req_data = request.get_json()

  if not req_data:
    abort(make_response(jsonify({'status': 400, 'message': 'No data provided'}), 400))

  data, errors = PoliticalPartySchema().load(req_data)
  if errors:
    abort(make_response(jsonify({'status': 400, 'message': 'Invalid data, please fill all required fields', 'errors': errors}), 400))

  if db.party_exists('name', data['name']):
        return jsonify({'status': 409, 'message' : 'Error party already exists'}), 409


  new_party = db.save(data)
  response = PoliticalPartySchema().dump(new_party).data
  return jsonify({
    'status': 201, 
    'data':[{
      'message': 'party created succesfully', 
      'party': response
    }]
  }), 201

@v1.route('/parties/<int:party_id>', methods=['GET'])
@jwt_required
def fetch_specific_party(party_id):
  """ 
    Endpoint for fetching a specific party
  """

  if not db.party_exists('id', party_id):
    abort(make_response(jsonify({
      'status': 404,
      'data':[{
      'message': 'party not found', 
      }] 
    }), 404))
  
  party = db.fetch_party_by_id(party_id)
  data = []
  data.append(PoliticalPartySchema().dump(party).data)
  return jsonify({
    'status': 200, 
    'data':[{
      'party': data
    }]
  }), 200

@v1.route('/parties', methods=['GET'])
@jwt_required
def fetch_all_parties():
  """
    Endpoint for fetching all political parties
  """

  parties = db.fetch_all_parties()
  response = PoliticalPartySchema(many=True).dump(parties).data
  return jsonify({
    'status': 200, 
    'data':[{
      'party': response
    }]
    }), 200


@v1.route('/parties/<int:party_id>/name', methods=['PATCH'])
@jwt_required
def update_party_name(party_id):
  """
    method to upvote a question
  """
  req_data = request.get_json()

  if not req_data:
    abort(make_response(jsonify({'status': 404, 'message': 'Error party not found'}), 404))

  data, errors = PoliticalPartySchema().load(req_data)
  if errors:
    abort(make_response(jsonify({'status': 400, 'message': 'Invalid data, please fill all required fields', 'errors': errors}), 400))

  if not db.party_exists('id', party_id):
    return jsonify({'status': 404, 'message': 'Error party not found!'}), 404

  party = db.update_party(party_id, data['name'])
  response = []
  response.append(PoliticalPartySchema().dump(party).data)
  return jsonify({
    'status': 200, 
    'data': [{
      'id': party_id,
      'name': data['name'],
      'message': 'party updated successfully', 
    }]
  }), 200