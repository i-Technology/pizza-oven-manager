import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from Pizza import Pizza

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

@anvil.server.callable
def publish_pizza(action,account,size,crust,toppings,price,status):
  print('Publishing')
  pizza=Pizza(action,account,size,crust,toppings,price,status)
  pizza.submit_pizza(action)
