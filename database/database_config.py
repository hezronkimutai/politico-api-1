import psycopg2
from werkzeug.security import generate_password_hash
import sys
import os
import logging
import psycopg2
from psycopg2.extras import RealDictCursor as dict_cursor
from instance.config import app_config

config_name = os.getenv('APP_SETTINGS')
    
# config = app_config[config_name]

# database = os.getenv('DATABASE_NAME')
# user = config.DATABASE_USERNAME
# password = config.DATABASE_PASSWORD
# host = config.DATABASE_HOST
# ort = config.DATABASE_PORT

# DSN = 'dbname={} user={} password={} host={} port={}'.format(
#   database, user, password, host, port
# )

# # try:
#   print(DSN) 
      
#   conn = psycopg2.connect(DSN)
#   cur = conn.cursor()

# except (Exception, psycopg2.DatabaseError) as error:
#   print(error)

# uri = DSN
#return connections
def connection(uri):
  con = psycopg2.connect(uri)
  return con

#returns connection and creates tables
def init_db(uri):
  con = connection(uri)
  cur = con.cursor()
  queries = tables()

  for query in queries:
    cur.execute(query)
  con.commit()

  return con

#returns connection and creates tables (TDD)
def init_test_db(test_uri):
  con = connection(test_uri)
  cur = con.cursor()
  queries = tables()

  for query in queries:
    cur.execute(query)
  con.commit()

  return con

#destroys all tables after tests have been ran
def destroydb():
  con = connection(test_uri)
  cur = con.cursor()
  users = """ DROP TABLE IF EXISTS users CASCADE; """
  parties = """ DROP TABLE IF EXISTS parties CASCADE; """
  offices = """ DROP TABLE IF EXISTS offices CASCADE; """
  queries = [users, parties, offices]

  for query in queries:
    cur.execute(query)
  con.commit()

#contains all talbes creation queiries
def create_tables():
  users = """ CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    firstname VARCHAR(20) NOT NULL,
    lastname VARCHAR(20) NOT NULL,
    othername VARCHAR(20),
    email VARCHAR(30) NOT NULL,
    phoneNumber VARCHAR(24) NOT NULL,
    password VARCHAR(1000) NOT NULL,
    passportUrl VARCHAR(256),
    isAdmin BOOLEAN DEFAULT FALSE,
    isPolitician BOOLEAN DEFAULT FALSE
  ); """

  parties = """ CREATE TABLE IF NOT EXISTS parties (
    id serial PRIMARY KEY NOT NULL,
    name VARCHAR(20) NOT NULL,
    hqAddress VARCHAR(24) NOT NULL, 
    logoUrl VARCHAR(256) NULL
  ); """

  offices = """ CREATE TABLE IF NOT EXISTS offices (
    id serial PRIMARY KEY NOT NULL,
    type VARCHAR(20) NOT NULL,
    name VARCHAR(20) NOT NULL 
  ); """

  queries = [users, parties, offices]
  return queries


def drop_all_tables():
  """ 
    Deletes all tables in the app 
  """

  tables_to_drop = drop_tables()
  for query in tables_to_drop:
    cur.execute(query)
    
  conn.commit

def fetch_one(query):
  """ 
    retreives a single row of data from a table 
  """
  self.cur.execute(query)
  fetchone = cur.fetchone()
  return fetchone

def save_updates(query):
  """ 
    saves data passed as a query to the stated table
  """
  cur.execute(query)
  conn.commit()

def fetch_all(query):
  """ 
    fetches all data stored
  """

  cur.execute(query)
  all_data = cur.fetchall()
  return all_data

def insert(query):
  """
    funcition that inserts news items into a table
  """
  cur.execute(query)
  data = cur.fetch_one()
  conn.commit()
  return data

  