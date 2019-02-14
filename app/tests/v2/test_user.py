from flask import json, make_response
from .base_test import BaseTest


class TestUser(BaseTest):
  """
    Test class for user endpoints
  """

  def setUp(self):
    """
      Initialize variables to be used for user tests
    """
    super().setUp()

  def get_value(self, data, key):
    new_value = data['data'][0]
    return new_value[key]
    
  def get_value2(self, data, key):
    new_value = data['data'][0]
    user_value = new_value['user']
    return user_value[key]
    
  def signup(self):
    """ 
      method to sign up user and get access token 
    """
        
    res = self.client.post('/api/v2/signup', json=self.super_user)
    data = res.get_json()
    data_token = self.get_value(data, 'access_token')

    self.access_token = data_token

  def test_index(self):
    """
      Tesst index welcome route
    """

    res = self.client.get('/api/v2/index', headers={'Content-Type': 'application/json'})
    data = res.get_json()

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['status'], 200)
    self.assertEqual(data['message'], 'welcome to Politico API Web service, use the base url: https://politco-api.herokuapp.com/api/v1 for posting your requests')

  def test_signup_with_no_data(self):
    """
      Test sign method up with no data
    """

    res = self.client.post('/api/v2/signup')
    data = res.get_json()

    self.assertEqual(res.status_code, 400)
    self.assertEqual(data['status'], 400)
    self.assertEqual(data['message'], 'No data provided')

  def test_signup_with_empty_data(self):
    """
      Test sign method up with empty data
    """

    user = {}

    res = self.client.post('/api/v2/signup', json=user, headers={'Content-Type': 'application/json'})
    data = res.get_json()

    self.assertEqual(res.status_code, 400)
    self.assertEqual(data['status'], 400)
    self.assertEqual(data['message'], 'No data provided')

  def test_signup_with_missing_fields(self):
    """
      Test signup method with missing fields 
    """

    user = {
      'firstname': 'Neville',
      'lastname': 'Oronni',
      'password': 'flask_is_awesome'
    }

    res = self.client.post('/api/v2/signup', json=user, headers={'Content-Type': 'application/json'})
    data = res.get_json()

    self.assertEqual(res.status_code, 400)
    self.assertEqual(data['status'], 400)
    self.assertEqual(data['message'], 'Invalid data, please fill all required fields')


  def test_signup_with_invalid_email(self):
    """
      Test sign method up with invalid email
    """

    user = {
      'firstname': 'Neville',
      'lastname': 'Oronni',
      'othername': 'Gerald',
      'email': 'wrong_email',
      'password': 'flask_is_awesome',
      'phoneNumber': '0799244265'
    }

    res = self.client.post('/api/v2/signup', json=user, headers={'Content-Type': 'application/json'})
    data = res.get_json()

    self.assertEqual(res.status_code, 400)
    self.assertEqual(data['status'], 400)
    self.assertEqual(data['message'], 'Invalid data, please fill all required fields')

  def test_signup_with_invalid_password(self):
    """ 
      Test signup method with invalid password
    """

    user = {
      "firstname": "Neville",
      "lastname": "Oronni",
      "othername": "Gerald",
      "email": "nevooronni@gmail.com",
      "password": "afdafs",
      "phoneNumber": "0799244265"
    }

    res = self.client.post('/api/v2/signup', json=user, headers={'Content-Type': 'application/json'})
    data = res.get_json()

    self.assertEqual(res.status_code, 400)
    self.assertEqual(data['status'], 400)
    self.assertEqual(data['message'], 'Invalid data, please fill all required fields')

  def test_signup_with_valid_data(self):
    """
      Test signup with valid data
    """

    user = {
      'firstname': 'Derrick',
      'lastname': 'Chisora',
      'email': 'derrick@gmail.com',
      'password': 'abcD$234g',
      'phoneNumber': '0725928106'  
    }

    res = self.client.post('/api/v2/signup', json=user, headers={'Content-Type': 'applicatioin/json'})
    data = res.get_json()

    self.assertEqual(res.status_code, 201)
    self.assertEqual(data['status'], 201)
    self.assertEqual( self.get_value(data, 'message'), 'User created successfully')
    self.assertEqual( self.get_value2(data, 'phoneNumber'), user['phoneNumber'])

  def test_signup_with_existing_email(self):
    """
      Test signup with an existing email address
    """

    user_1 = {
      'firstname': 'Frank',
      'lastname': 'Ekirapa',
      'email': 'frankekirapa254@gmail.com',
      'password': 'abcD$234g',
      'phoneNumber': '0712345678'  
    }

    res_1 = self.client.post('/api/v2/signup', json=user_1, headers={'Content-Type': 'application/json'})
    data_1 = res_1.get_json()

    self.assertEqual(res_1.status_code, 201)
    self.assertEqual(data_1['status'], 201)

    user_2 = {
      'firstname': 'Jane',
      'lastname': 'Onimbo',
      'email': 'frankekirapa254@gmail.com',
      'password': 'rbcF$214c',
      'phoneNumber': '0712344444'  
    }

    res_2 = self.client.post('/api/v2/signup', json=user_2, headers={'Content-Type': 'application/json'})
    data_2 = res_2.get_json()

    self.assertEqual(res_2.status_code, 409)
    self.assertEqual(data_2['status'], 409)
    self.assertEqual(data_2['message'], 'Error email already exists')

  def test_signup_with_existing_phonenumber(self):
    """
      Test sign up with an existing phonenumber
    """
    user_1 = {
      'firstname': 'William',
      'lastname': 'Wamarite',
      'email': 'William@gmail.com',
      'password': 'abcD$234g',
      'phoneNumber': '0782444525'  
    }

    res_1 = self.client.post('/api/v2/signup', json=user_1, headers={'Content-Type': 'application/json'})
    data_1 = res_1.get_json()

    self.assertEqual(res_1.status_code, 201)
    self.assertEqual(data_1['status'], 201)

    user_2 = {
      'firstname': 'Paul',
      'lastname': 'Davis',
      'email': 'william@gmail.com',
      'password': 'rbcF$214c',
      'phoneNumber': '0782444525'  
    }

    res_2 = self.client.post('/api/v2/signup', json=user_2, headers={'Content-Type': 'application/json'})
    data_2 = res_2.get_json()

    self.assertEqual(res_2.status_code, 409)
    self.assertEqual(data_2['status'], 409)
    self.assertEqual(data_2['message'], 'Error phone number already exists')
