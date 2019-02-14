from marshmallow import Schema, fields, post_dump
from ...v1.utils.validators import email, password, required
from ..models.user_model import User

class UserSchema(Schema):
  """
    User class to validate schema for user object
  """

  id = fields.Int(dump_only=True)
  firstname = fields.Str(required=True, validate=(required))
  lastname = fields.Str(required=True, validate=(required))
  othername = fields.Str(required=False)
  phoneNumber = fields.Str(required=True, validate=(required))
  email = fields.Email(required=True, validate=(email))
  password = fields.Str(required=True, validate=(password))
  passportUrl = fields.Str(required=False)
  isAdmin = fields.Bool(dump_only=True)
  isPolitician = fields.Bool(dump_only=True)

