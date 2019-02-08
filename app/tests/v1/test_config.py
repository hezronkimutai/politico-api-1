import unittest
from app import create_app

class TestDevelopmentConfig(unittest.TestCase):
  """
    Test class for development config
  """

  def setUp(self):
    self.app = create_app('development')

  def test_app_is_in_development_mode(self):
    """
      Test method for development environment
    """

    self.assertEqual(self.app.config['DEBUG'], True)
    self.assertEqual(self.app.config['TESTING'], False)

  def tearDown(self):
    self.app = None

class TestTestingConfig(unittest.TestCase):
  """
    Test class for testing config
  """
  def setUp(self):
    self.app = create_app('testing')

  def test_app_is_in_testing_mode(self):
    """
      Test method for testing environment
    """
    self.assertEqual(self.app.config['DEBUG'], True)
    self.assertEqual(self.app.config['TESTING'], True)

  def tearDown(self):
    self.app = None

class TestStagingConfig(unittest.TestCase):
  """
    Test class for staging config
  """

  def setUp(self):
    self.app = create_app('staging')

  def test_app_is_in_staging_mode(self):
    """
      Test method for staging environment
    """

    self.assertEqual(self.app.config['DEBUG'], True)
    self.assertEqual(self.app.config['TESTING'], False)

  def tearDown(self):
    self.app = None

class TestProductionConfig(unittest.TestCase):
  """
    Test class for production config
  """

  def setUp(self):
    self.app = create_app('production')

  def test_app_is_in_production_mode(self):
    """
      Test method for production environment
    """

    self.assertEqual(self.app.config['DEBUG'], False)
    self.assertEqual(self.app.config['TESTING'], False)

  def tearDown(self):
    self.app = None