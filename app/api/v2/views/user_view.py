from flask import jsonify, request, abort, make_response
from flask.views import MethodView
from ..schemas.user_schema import UserSchema
from ..models.user_model import User
from datetime import timedelta
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,get_jwt_identity, jwt_refresh_token_required, get_raw_jwt)

db = User()

class IndexAPI(MethodView):
  """
    class for index route endpoint
  """

  def get(self):
    return jsonify({
      'status': 200,
      'message': 'welcome to Politico API Web service, use the base url: https://politco-api.herokuapp.com/api/v1 for posting your requests'
    })


class UserSignupAPI(MethodView):
  """
    class for user route endpoint
  """
  
  def post(self):
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
      print(str(new_user))

      # Generate access 
      access_token = create_access_token(identity=new_user[0], fresh=True)
      refresh_token = create_refresh_token(identity=new_user[0])
      return jsonify({
          'status': 201, 
          'data': [{
            'user': result,
            'message' : 'User created successfully', 
            'access_token' : access_token, 
            'refresh_token' : refresh_token 
            }] 
          }), 201

# class UserSigninAPI(MethodView):
#   """
#     class for user signin endpoints
#   """

#   def post(self):
#     """
#       Endpoint function to signin an existing user
#     """
#     signin_data = request.get_json()

#     if not signin_data:
#       abort(make_response(jsonify({
#         'status': 400, 'message': 
#         'No data provided', 
#       }), 400))

#     data, errors = UserSchema().load(signin_data, partial=True)
#     if errors:
#       abort(make_response(jsonify({'status': 400, 'message': 'Invalid data, please fill all required fields', 'errors': errors}), 400))

#     try:
#       username = data['phoneNumber']
#       password = data['password']
#     except:
#       abort(make_response(jsonify({'status': 400, 'message': 'Invalid credentials'}), 400))

#     if not db.user_exists('phoneNumber', data['phoneNumber']):
#       abort(make_response(jsonify({'status': 404, 'message': 'user not found'}), 404))

#     user = db.find_user_by_phonenumber('phoneNumber', data['phoneNumber'])
#     db.check_password(user['password'], password)

#     #generate access token
#     access_token = create_access_token(identity=user['id'], fresh=True)
#     refresh_token = create_refresh_token(identity=True)
#     return jsonify({
#       'status': 200,
#         'data': [{
#           'message': 'user logged in succesfully',
#           'access_token': access_token,
#           'refresh_token': refresh_token
#         }] 
#       }), 200

class TokenAPI(MethodView):
  """
    class for jwt endpoints
  """

  @jwt_refresh_token_required
  def post(self):
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

index_view = IndexAPI.as_view('index_api') 
signup_auth_view = UserSignupAPI.as_view('signup_auth_api')
token_view = TokenAPI.as_view('token_api')


