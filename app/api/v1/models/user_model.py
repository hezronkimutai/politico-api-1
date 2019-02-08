from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from ..utils.utils import generate_id

users = []

class User(object):
  """
    Model class for user object
  """

  def save(self, data):
    """
      method to save new user
    """

    data['id'] = generate_id(users)
    data['password'] = generate_password_hash(data['password'])
    data['createdOn'] = datetime.now()
    data['isAdmin'] = False

    users.append(data)
    return data
    
  def user_exists(self, key, value):
    """
     method to check if a user exists
    """

    got_user = [user for user in users if value == user[key]]
    return len(got_user) > 0

  def find_user_by_phonenumber(self, key, phoneNumber):
    """
      method to find a user by username
    """
    got_user = [user for user in users if user['phoneNumber'] == phoneNumber]
    return got_user[0]

  def check_password(self, hash, password):
    """
      method to check if the passwords match
    """

    return check_password_hash(hash, password)

