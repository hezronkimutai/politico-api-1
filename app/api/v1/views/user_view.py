from flask import jsonify, request, abort, make_response
from ...v1 import version_1 as v1
from ..schemas.user_schema import UserSchema
from ..models.user_model import User
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,get_jwt_identity, jwt_refresh_token_required, get_raw_jwt)

db = User()

@v1.route('/', methods=['GET'])
@v1.route('/index', methods=['GET'])
def index():
    return jsonify({
      'status': 200, 
      'message': 'Welcome to Politico API web service!'
    }), 200

@v1.route('/signup', methods=['POST'])
def signup():
    """ Endpoint functiom to register new user """
    res_data = request.get_json()

    if not res_data:
        return jsonify({'status': 400, 'message': 'No data provided'}), 400

    data, errors = UserSchema().load(res_data)
    if errors:
        return jsonify({'status': 400, 'message' : 'Invalid data, please fill all required fields', 'errors': errors}), 400

    if db.user_exists('phoneNumber', data['phoneNumber']):
        return jsonify({'status': 409, 'message' : 'Error phone number already exists'}), 409

    if db.user_exists('email', data['email']):
        return jsonify({'status': 409, 'message' : 'Error email already exists'}), 409

    new_user = db.save(data)
    result = UserSchema(exclude=['password']).dump(new_user).data

    # Generate access 
    access_token = create_access_token(identity=new_user['id'], fresh=True)
    refresh_token = create_refresh_token(identity=new_user['id'])
    return jsonify({
        'status': 201, 
        'data': [{
          'user': result,
          'message' : 'User created successfully', 
          'access_token' : access_token, 
          'refresh_token' : refresh_token 
          }] 
        }), 201

@v1.route('/refresh-token', methods=['POST'])
@jwt_refresh_token_required
def refresh_token():
  """
    Endpoint function to refresh tokens
  """
  current_user = get_jwt_identity()
  access_token = create_access_token(identity=current_user)
  return jsonify({
      'status': 200, 
      'message': 'Token refreshed succesfully', 
      'access_token': access_token
    }), 200

@v1.route('/signin', methods=['POST'])
def signin():
  """
    Endpoint function to signin an existing user
  """
  signin_data = request.get_json()

  if not signin_data:
    abort(make_response(jsonify({
      'status': 400, 'message': 
      'No data provided', 
      }), 400))

  data, errors = UserSchema().load(signin_data, partial=True)
  if errors:
    abort(make_response(jsonify({'status': 400, 'message': 'Invalid data, please fill all required fields', 'errors': errors}), 400))

  try:
    username = data['phoneNumber']
    password = data['password']
  except:
    abort(make_response(jsonify({'status': 400, 'message': 'Invalid credentials'}), 400))

  if not db.user_exists('phoneNumber', data['phoneNumber']):
    abort(make_response(jsonify({'status': 404, 'message': 'user not found'}), 404))

  user = db.find_user_by_phonenumber('phoneNumber', data['phoneNumber'])
  db.check_password(user['password'], password)

  #generate access token
  access_token = create_access_token(identity=user['id'], fresh=True)
  refresh_token = create_refresh_token(identity=True)
  return jsonify({
    'status': 200,
    'data': [{
      'message': 'user logged in succesfully',
      'access_token': access_token,
      'refresh_token': refresh_token
    }] 
  }), 200
