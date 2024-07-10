import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from Pizza import Pizza

#

#anvil.server.call('publish_pizza', 'Update', self.account, self.size, self.crust, self.toppings, self.price,self.status)
@anvil.server.callable
def publish_pizza(action,eventz_id,account,size,crust,toppings,price,status):
  print('Publishing3', action, status)
  pizza=Pizza(action,eventz_id,account,size,crust,toppings,price,status)
  print('at 25', pizza,pizza.eventz_id)
  eid = pizza.submit_pizza(action)
  print('at 27 pizza_eventz_id', pizza.eventz_id, eid)
  return eid

      #anvil.server.call('publish_pizza', 'Update', self.eventz_id, self.account, self.size, self.crust, self.toppings, self.price1.text,self.status)
@anvil.server.callable
def put_pizza_in_table(eventz_id,account,size,crust,toppings,price,status):
  action = 'None'
  #pizza=Pizza(action,eventz_id,account,size,crust,toppings,price,status)
  app_tables.pizza_oven.add_row(eventz_id=eventz_id,account_no=account,size=size, crust=crust, toppings=str(toppings), price=float(price),status=status)
  print('369 finished inserting table')

@anvil.server.callable
def get_pizzas():
    # Fetch all rows from the pizzas table
    return app_tables.pizza_oven.search()

@anvil.server.callable
def put_account_in_table(eventz_id,phone,name,address,email):
  action = 'None'
  #pizza=Pizza(action,eventz_id,account,size,crust,toppings,price,status)
  app_tables.pizza_oven.add_row(eventz_id=eventz_id,account_no=account,size=size, crust=crust, toppings=str(toppings), price=float(price),status=status)
  print('369 finished inserting table')
