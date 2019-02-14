""" 
  Main connection to the postgres database 
"""

import sys
import os
import logging
import psycopg2
from .database_config import create_tables, destroydb
from psycopg2.extras import RealDictCursor as dict_cursor
from instance.config import app_config

class DatabaseConnection:
  """ 
    Handles the main connection to the database of the app setting 
  """

  def __init__(self, config_name):
    """
      initialize the class instance to take a database url as a parameter
    """

    config = app_config[config_name]

    database = config.DATABASE_NAME
    user = config.DATABASE_USERNAME
    password = config.DATABASE_PASSWORD
    host = config.DATABASE_HOST
    port = config.DATABASE_PORT

    DSN = 'dbname={} user={} password={} host={} port={}'.format(
      database, user, password, host, port
    )
        
    try:
      if config_name == 'testing':

        database_test = config.DATABASE_TEST_NAME
        DSN = 'dbname={} user={} password={} host={} port={}'.format(
          database_test, user, password, host, port
        )
        print(DSN) 

        self.conn = psycopg2.connect(DSN)
        self.cur = self.conn.cursor()

        self.drop_all_tables()
        self.create_tables()
        self.create_admin(self.conn)

      else: 
        print(DSN) 
        
        self.conn = psycopg2.connect(DSN)
        self.cur = self.conn.cursor()

        self.drop_all_tables()
        self.create_tables()

    except (Exception, psycopg2.DatabaseError) as error:
      print("Database Error" + str(error))

  def create_tables(self):
    """ 
      creates all tables 
    """

    all_tables_to_create = create_tables()
    for query in all_tables_to_create:
      self.cur.execute(query)
      
    self.conn.commit()
    
  def create_admin(self, conn):
    """ 
      create admin after creating tables
    """
    query = "INSERT INTO users (firstname, lastname, othername, phoneNumber, email,\
      password, isAdmin, isPolitician) VALUES ('Neville', 'Oronni', 'Gerald', '0712345678',\
      'nevooronni@gmail.com', 'abc1$#De0', True, False)"

    self.cur.execute(query)
    self.conn.commit()

  def insert(self, query):
    """
      funcition that inserts new items into a table
    """
    self.cur.execute(query)
    data = self.cur.fetchone()
    return data

  def fetch_one(self, query):
    """ 
      retreives a single row of data from a table 
    """
    self.cur.execute(query)
    fetchone = self.cur.fetchone()
    return fetchone

  def save_updates(self, query):
    """ 
      saves data passed as a query to the stated table
     """
    self.cur.execute(query)
    self.conn.commit()

  def fetch_all_data(self, query):
    """ 
      fetches all data stored
    """

    self.cur.execute(query)
    fetch_all = self.cur.fetchall()
    return fetch_all

  def drop_tables(self):
    """
      function for drop database tables
    """

    drop_users = """ DROP TABLE IF EXISTS users """
    drop_parties = """ DROP TABLE IF EXISTS parties """
    drop_offices = """ DROP TABLE IF EXISTS offices """

    return [drop_users, drop_parties, drop_offices]

  def drop_all_tables(self):
    """ 
      Deletes all tables in the app 
    """

    tables_to_drop = self.drop_tables()
    for query in tables_to_drop:
      self.cur.execute(query)
    
    self.conn.commit