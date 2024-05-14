from ._anvil_designer import Pizza_OvenTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Pizza_Oven(Pizza_OvenTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.hidden_columns = []
    self.init_components(**properties)
    
    #anvil.users.login_with_form()
#     self.pizza_size = 'Small'
#     self.pizza_size_price = 10.0
#     self.item['crust'] = 'Thin'
#     self.pizza_crust = 'Thin'   
    self.account = 0  # Initialize the account variable
    self.repeating_panel_1.items = anvil.server.call('get_pizza')
    
#      # Get the columns of the DataGrid
#     columns = self.data_grid_1.columns

#     # Find the column you want to hide
#     for column in columns:
#       print(f"column_data_key: {column['data_key']}")
#       if column['data_key'] == 'eventz_id':
#         print('29 fired!')
#         column['visible'] = False

#     # Optionally, update the DataGrid to refresh the view 
#     self.data_grid_1.columns = columns
    # Filter the column with title 'Stock Price' out of the columns list.
    column = [c for c in self.data_grid_1.columns if c['data_key'] == 'eventz_id'][0]
#     column = [c for c in self.data_grid_1.columns if c['title'] == 'Stock Price'][0] 
    
    # Remember the details of the hidden column
    self.hidden_columns.append(column)
    
    # Remove it from the Data Grid's column list
    self.data_grid_1.columns.remove(column)
    
    # Make the change live
    self.data_grid_1.columns = self.data_grid_1.columns
    
    
    
   # Additional UI setup
   # self.setup_price_tb()   
    
   # self.calculate_price()
    #self.pizza_list_show()