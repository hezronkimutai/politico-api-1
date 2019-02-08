revoked_tokens = []

class RevokedTokenModel(object):
  """
    Model class for revoked tokens
  """
  def add(self, jti):
    """
      method to save token id
    """
    revoked_tokens.append(jti)

  def is_blacklisted(self, jti):
    """
      method to check if token id is blacklisted
    """
    return bool(jti in revoked_tokens)