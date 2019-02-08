from datetime import datetime
from ..utils.utils import generate_id

class Model(object):
  """
    Base model class
  """

  from datetime import datetime
from ..utils.utils import generate_id

class Model(object):
  """
    Base model class
  """

  def __init__(self, collection):
    """
      initializes list of an object type
    """
    self.collection = collection

  def save(self, data):
    """
      method to save object
    """
    data['createdOn'] = datetime.now()
    self.collection.append(data)
    return data

  def check_if_it_exists(self, key, value):
    """
      method to check if an object exist using key, value pair
    """
    items = [item for item in self.collection if item[key] == value]
    return len(items) > 0

  def find(self, key, value):
    """
      method to find object item using key, value pair
    """
    items = [item for item in self.collection if item[key] == value]
    return items[0]

  def fetch_all(self):
    """
      method to fetch all items objects
    """
    return self.collection

  def delete(self, id):
    """
      method to delete item object
    """
    item = self.find('id', id)
    self.collection.remove(item)