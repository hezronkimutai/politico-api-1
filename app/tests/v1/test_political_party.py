from flask import json
from .base_test import BaseTest
from app.api.v1.models.political_party_model import political_parties
from app.api.v1.models.user_model import users


class TestPoliticalParty(BaseTest):
  """
    Test class for a political party
  """

  def setUp(self):
    """
      setup method for initializing varialbes
    """
    super().setUp()

    self.super_user = {
      'firstname': 'Donald',
      'lastname': 'Trump',
      'email': 'trump@gmail.com',
      'password': 'abcD$234g',
      'phoneNumber': '0781818181'
    }

    self.political_party = {
      'name': 'Jubilee Party',
      'hqAddress': '14/01/2019',
      'logoUrl': 'app/img/party.jpg'
    }

    self.political_party_2 = {
      'name': 'Jubilee Party',
      'hqAddress': 'Pangani, Nairobi',
      'logoUrl': 'app/img/jubilee.jpg'
    }

    self.party_with_no_name = {
      'hqAddress': 'Kasarani, Nairobi',
      'logoUrl': 'app/img/party.jpg'
    }

    self.party_with_empty_name = {
      'name': '',
      'hqAddress': 'Pangani, Nairobi',
      'logoUrl': 'app/img/party.jpg'  
    }

    self.res_1 = self.client.post('/api/v1/signup', json=self.super_user, headers={'Content-Type': 'application/json'})
    self.data_1 = self.res_1.get_json()
    self.data_1_token = self.get_value(self.data_1, 'access_token')


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
        
    res = self.client.post('/api/v1/signup', json=self.super_user)
    data = res.get_json()
    data_token = self.get_value(data, 'access_token')

    self.access_token = data_token

    return self.access_token

  def tearDown(self):
    """
      teardown method empty all initialized variables
    """

    political_parties.clear()
    super().tearDown()
    users.clear()

  def test_create_party_with_no_data(self):
    """
      Test create party with no data provided
    """
    
    res = self.client.post('/api/v1/parties', headers={'Authorization': 'Bearer {}'.format(self.data_1_token)})
    data = res.get_json()

    self.assertEqual(res.status_code, 400)
    self.assertEqual(data['status'], 400)
    self.assertEqual(data['message'], 'No data provided')

  def test_create_party_with_empty_data(self):
    """
      Test create party method with emtpy data
    """

    party = {}
    res = self.client.post('/api/v1/parties', json=json.dumps(party), headers={'Authorization': 'Bearer {}'.format(self.data_1_token)})
    data = res.get_json()

    self.assertEqual(res.status_code, 400)
    self.assertEqual(data['status'], 400)
    self.assertEqual(data['message'], 'Invalid data, please fill all required fields')

  def test_create_party_with_missing_fields(self):
    """
      Test create party method with missing fields
    """

    res = self.client.post('/api/v1/parties', json=self.party_with_no_name, headers={'Authorization': 'Bearer {}'.format(self.data_1_token)})
    data = res.get_json()

    self.assertEqual(res.status_code, 400)
    self.assertEqual(data['status'], 400)
    self.assertEqual(data['message'], 'Invalid data, please fill all required fields')

  def test_create_party_with_empty_fields(self):
    """
      Test create party method with empty fields
    """

    res = self.client.post('/api/v1/parties', json=self.party_with_empty_name, headers={'Authorization': 'Bearer {}'.format(self.data_1_token)})
    data = res.get_json()

    self.assertEqual(res.status_code, 400)
    self.assertEqual(data['status'], 400)
    self.assertEqual(data['message'], 'Invalid data, please fill all required fields')

  def test_create_party_with_existing_name(self):
    """
      Test create party with an existing name method
    """

    data_1 = self.res_1.get_json()
    data_1_token = self.get_value(data_1, 'access_token')

    res = self.client.post('/api/v1/parties', json=self.political_party, headers={'Authorization': 'Bearer {}'.format(data_1_token)})
    data_1 = res.get_json()

    self.assertEqual(res.status_code, 201)
    self.assertEqual(data_1['status'], 201)

    res_2 = self.client.post('/api/v1/parties', json=self.political_party_2, headers={'Authorization': 'Bearer {}'.format(data_1_token)})
    data_2 = res_2.get_json()

    self.assertEqual(res_2.status_code, 409)
    self.assertEqual(data_2['status'], 409)
    self.assertEqual(data_2['message'], 'Error party already exists')

  def test_create_party(self):
    """
      Test create party method
    """
    data_1 = self.res_1.get_json()

    data_1_token = self.get_value(data_1, 'access_token')

    res = self.client.post('/api/v1/parties', json=self.political_party, headers={'Authorization': 'Bearer {}'.format(data_1_token)})
    data = res.get_json()

    self.assertEqual(res.status_code, 201)
    self.assertEqual(data['status'], 201)
    self.assertEqual(self.get_value(data, 'message'), 'meetup created succesfully')


  