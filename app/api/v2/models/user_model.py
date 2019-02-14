# from ....database_config import init_db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
from database.database import DatabaseConnection

table = 'users'
config_name = os.getenv('APP_SETTINGS')

class User(object):
  """
    Model class for user object
  """

  def save(self, data):
    """
      method to save new user
    """
    password = generate_password_hash(data['password'])

    query = "INSERT INTO {} (firstname, lastname, password, phoneNumber, email) VALUES ('{}', '{}', '{}', '{}', '{}') RETURNING *".format(
        table, data['firstname'], 
        data['lastname'], data['password'], data['phoneNumber'], data['email']
      )

    return DatabaseConnection(config_name).insert(query)

  def user_exists(self, key, value):
    """
     method to check if a user exists
    """

    query = "SELECT * FROM {} WHERE {} = '{}'".format(
      table, key, value) 

    got_user = DatabaseConnection(config_name).fetch_all_data(query)
    return len(got_user) > 0
  
  def find_user_by_phonenumber(self, key, phoneNumber):
    """
      method to find a user by username
    """
    query = "SELECT * FROM {} WHERE {} = '{}'".format(
      table, key, phoneNumber) 

    got_user = DatabaseConnection(config_name).fetch_one(query)
    return got_user

  def check_password(self, hash, password):
    """
      method to check if the passwords match
    """

    return check_password_hash(hash, password)

