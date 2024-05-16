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

class Pizza(object):
  def __init__(self,action,eventz_id,account,size,crust,toppings,price,status):
    self.record_id  = ''  # This is not used as of May 16-24
    self.action = action
    self.size = size
    self.crust = crust
    self.toppings = toppings
    self.price = price
    self.status = status
    self.publisher = Publisher()
    self.account=account
    self.eventz_id = eventz_id  # This is the eventz record id (UUID) assigned by Publisher
    
  def load_pizza(self,eventz_id,account,size,crust,toppings,price,status):
    
    self.size = size
    self.crust = crust
    self.toppings = toppings
    self.price = price
    self.status = status
    self.eventz_id = eventz_id
    
  def make_tuple(self):
    record_tuple = (self.account,self.size, self.crust, self.toppings, self.price, self.status)
    print('at 47 record_tuple', record_tuple,self.price)
    return record_tuple
  
  
  def submit_pizza(self,action):
    print ('at 50 submit pizza')
    record_tuple = self.make_tuple()
    print('at 52', record_tuple, action)
    if action == 'New':
      published_record = self.publisher.publish(500001.00, record_tuple, RecordAction.INSERT.value)
      er = ast.literal_eval(str(published_record))
      print(f'er: {er}')
      eventz_id = er[2]
      print(f'Published Record: {published_record}   Eventz Id: {eventz_id}')
      app_tables.pizzas.add_row(events_id=eventz_id,account=self.account,size=self.size, crust= self.crust, toppings= self.toppings, price= self.price)
    elif action == 'Update':
      print ('at 60 updating', self.eventz_id)
      old_eventz_id = self.eventz_id
      print ('at 63', old_eventz_id)
      published_record = self.publisher.publish(500001.00, record_tuple, str(RecordAction.UPDATE.value),link = old_eventz_id)
      print ('at 65 ', record_tuple)
      er = ast.literal_eval(str(published_record))
      print(f'er: {er}')
      self.eventz_id = er[2]
      print(f'Published Record: {published_record}   Eventz Id: {self.eventz_id}')
#       app_tables.pizza_oven.add_row(eventz_id=eventz_id,account_no=self.account,size=self.size, crust= self.crust, toppings= self.toppings, price= self.price)
      print('at 70', old_eventz_id)
      row =app_tables.pizza_oven.get(eventz_id = old_eventz_id)
      print('at 74', row)
      row.update(eventz_id = self.eventz_id, account_no=self.account, size=self.size, crust= self.crust, toppings= self.toppings, price= self.price)
    elif action == 'Delete':
      old_eventz_id = eventz_id
      eventz_id = self.publisher.publish(500001.00, record_tuple, RecordAction.DELETE.value,link = old_eventz_id)[2]
      row =app_tables.pizzas.get(eventz_id = old_eventz_id)
      for row in rows: row.delete()
      
    else:
      print(f'Invalid action! {action}')
      
    return self.eventz_id
    
