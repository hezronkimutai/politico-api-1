"""App configurations"""

import os

class Config(object):
  """
    Parent configuration class.
  """
  DEBUG = False
  TESTING = False
  JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
  SECRET_KEY = os.getenv('SECRET_KEY')
  JWT_BLACKLIST_ENABLED = True
  JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

class DevelopmentConfig(Config):
  """
    Configurations for Development.
  """
  DEBUG = True

class TestingConfig(Config):
  """
    Configuration for Testing with a seperate test database.
  """

  TESTING = True
  DEBUG = True

class StagingConfig(Config):
  """
    Configuration for Staging
  """
  DEBUG = True

class ProductionConfig(Config):
  """
    Configuration for Production
  """

  DEBUG = False
  TESTING = False

app_config = {
  'development': DevelopmentConfig,
  'testing': TestingConfig,
  'staging': StagingConfig,
  'production': ProductionConfig,
}
