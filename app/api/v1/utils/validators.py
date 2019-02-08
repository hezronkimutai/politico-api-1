import re
from marshmallow import ValidationError

def required(value):
  """
    validate field does not contain a null value.
  """

  if isinstance(value, str):
    if not value.strip(' '):
      raise ValidationError('This parameter cannot be null')
    return value
  elif value:
    return value

def email(value):
  """
    Function to validate email format
  """

  if not re.match(r"(^[a-zA-z0-9_.]+@[a-zA-z0-9]+\.[a-z]+$)", value):
    raise ValidationError('Invalid email format')

  return value

def password(password):
  """
    Function to validate if password is strong
  """

  error = False
  while True:
    if (len(password)<8):
      error = True
      break
    elif not re.search("[a-z]", password):
      error = True
      break
    elif not re.search("[A-Z]", password):
      error = True
      break
    elif not re.search("[0-9]", password):
      error = True
      break
    elif not re.search("[_@$#&^%]", password):
      error = True
      break
    elif re.search("\s", password):
      error = True
      break
    else:
      break

  if error == True:
    raise ValidationError('Weak password provided')