from flask import jsonify, request, abort, make_response
from flask.views import MethodView
# from ...v1 import version_1 as v1
from ..schemas.office_schema import OfficeSchema
from ..models.office_model import Office
from flask_jwt_extended import (jwt_required, get_jwt_identity)

db = Office()

class PolitcalOfficeAPI(MethodView):
  """
    class for political office method views
  """

  @jwt_required
  def post(self):
    """
      Endpoint for creating a office
    """
    req_data = request.get_json()

    if not req_data:
      abort(make_response(jsonify({'status': 400, 'message': 'No data provided'}), 400))

    data, errors = OfficeSchema().load(req_data)
    if errors:
      abort(make_response(jsonify({'status': 400, 'message': 'Invalid data, please fill all required fields', 'errors': errors}), 400))

    if db.office_exists('name', data['name']):
          return jsonify({'status': 409, 'message' : 'Error office already exists'}), 409


    new_office = db.save(data)
    response = OfficeSchema().dump(new_office).data
    return jsonify({
      'status': 201, 
      'data':[{
        'message': 'office created succesfully', 
        'office': response
      }]
    }), 201

  @jwt_required
  def get(self, office_id):
    """ 
      Endpoint for fetching a specific office
    """
    
    if not db.office_exists('id', office_id):
      abort(make_response(jsonify({
        'status': 404,
        'data':[{
        'message': 'office not found', 
        }] 
      }), 404))
    
    office = db.fetch_office_by_id(office_id)
    data = []
    data.append(OfficeSchema().dump(office).data)
    return jsonify({
      'status': 200, 
      'data':[{
        'office': data
      }]
    }), 200

  @jwt_required
  def delete(self, office_id):
    """
      method to delete an office
    """

    if not db.office_exists('id', office_id):
      return jsonify({'status': 404, 'message': 'Error office not found'}), 404
    else: 
      db.delete(office_id)
    
    return jsonify({
      'status': 200, 
      'data': [{
        'message': 'office deleted successfully', 
      }]
    }), 200



class AllPolitcalOfficeAPI(MethodView):
  """
    class for all politcal office method views
  """

  @jwt_required
  def get(self):
    """
      Endpoint for fetching all political offices
    """

    offices = db.fetch_all_offices()
    response = OfficeSchema(many=True).dump(offices).data
    return jsonify({
      'status': 200, 
      'data':[{
        'offices': response
      }]
      }), 200

create_office_view = PolitcalOfficeAPI.as_view('create_office_api')
fetch_office_view = PolitcalOfficeAPI.as_view('fetch_office_api')
fetch_all_offices_view = AllPolitcalOfficeAPI.as_view('fetch_all_offices_view')
delete_office_view = PolitcalOfficeAPI.as_view('delete_office_api')


