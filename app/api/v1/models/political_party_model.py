from datetime import datetime
from ..utils.utils import generate_id
from .base_model import Model

political_parties = []

class PoliticalParty(Model):
  """
    Class for meetup object
  """

  def __init__(self):
    super().__init__(political_parties)

  def save(self, data):
    """
      method to add a new meetup
    """

    data['id'] = generate_id(self.collection)
    return super().save(data)

  def party_exists(self, key, value):
    """
     method to check if a party exists
    """

    got_party = [party for party in political_parties if value == party[key]]
    return len(got_party) > 0

  # def fetch_meetup_by_id(self, id):
  #   """
  #     method for fetching a meetup by id
  #   """

  #   meetups_fetched = [meetup for meetup in meetups if meetup['id'] == id]

  #   return meetups_fetched[0]