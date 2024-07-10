import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import ast
from EventzAnvilAPI import Publisher, Subscriber, RecordAction, LibrarianClient

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
class Account(object):
  def __init__(self,action,phone, name, address, email):
    self.record_id  = ''
    self.action = action
    self.phone = phone
    self.name = name
    self.address = address
    self.email = email
    self.publisher = Publisher()
    
  def make_tuple(self):
    record_tuple = (self.phone, self.name, self.address, self.email)
    return record_tuple
  
  
  def submit_account(self,action):
    record_tuple = self.make_tuple()
