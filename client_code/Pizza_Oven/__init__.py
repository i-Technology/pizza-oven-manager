from ._anvil_designer import Pizza_OvenTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Pizza_Oven(Pizza_OvenTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.

    self.init_components(**properties)
    #anvil.users.login_with_form()
    self.pizza_size = 'Small'
    self.pizza_size_price = 10.0
    self.item['crust'] = 'Thin'
    self.pizza_crust = 'Thin'
#     self.crust_price = 1.0
    self.toppings = 0 # Integer # of toppings selected now
#     self.top_price = 0.1
#     self.price = 0.00
    #self.item['account'] = 0
    
    self.account = 0  # Initialize the account variable
    self.repeating_panel_1.items = app_tables.pizza_oven.search()
    
   # Additional UI setup
   # self.setup_price_tb()   
    
   # self.calculate_price()
    #self.pizza_list_show()