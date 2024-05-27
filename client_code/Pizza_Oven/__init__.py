from ._anvil_designer import Pizza_OvenTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

#ToDo: 
#ToDo: Format price on form
#ToDo: 
#ToDo: 

class Pizza_Oven(Pizza_OvenTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.hidden_columns = []
    self.init_components(**properties)
    self.nnn = 0
    
    # print("Launching Subscriber!")    
    # self.subscriber_task = anvil.server.call('launch_subscriber_task')

    print("Starting Timer")
    self.timer_1.interval = 1  # 1 second
    #anvil.users.login_with_form()
#     self.pizza_size = 'Small'
#     self.pizza_size_price = 10.0
#     self.item['crust'] = 'Thin'
#     self.pizza_crust = 'Thin'   
    self.account = 0  # Initialize the account variable
    self.repeating_panel_1.items = anvil.server.call('get_pizza')

    # Filter the column with title 'Stock Price' out of the columns list.
    column = [c for c in self.data_grid_1.columns if c['data_key'] == 'eventz_id'][0]
#     column = [c for c in self.data_grid_1.columns if c['title'] == 'Stock Price'][0] 
    
    # Remember the details of the hidden column
    self.hidden_columns.append(column)
    
    # Remove it from the Data Grid's column list
    self.data_grid_1.columns.remove(column)
    
    # Make the change live
    self.data_grid_1.columns = self.data_grid_1.columns


  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""

    message =  anvil.server.call("get_message")
   #print ('at 451', message)
    self.nnn += 1
    #print('687 Ticked to: ', self.nnn)
    if message != 'None':
      print('55a', message)
      action = message[1]   # Could be out of range -- Nope! Can't get here.
      print(f'57a {type(action)} -{action}-')
      if action == 0:   # Process only New records. Ignore Updates and Deletes.       
        record_type = message[0]   # 500001.00
        if record_type == '500001.00':        
          record_id = message[2]# '67fd1474-a823-42b7-802b-ad304a757022'
          link_id = message[3] #  '00000000-0000-0000-0000-000000000000'
          time = message[6]
          account = message[16]
          size = message[17]
          crust = message[18]
          toppings = message[19]
          price = message[20]
          status = message[21]
  
          #print (record_type, record_id, link_id, time, account, size, crust, toppings, price, status)  # QC check
          anvil.server.call ('put_pizza_in_table', record_id,account,size,crust,toppings,price,status)       
          print('641 got here. Now refreshing data grid.')
  
          self.refresh_data_grid()

       
 #['500001.00', 0, '67fd1474-a823-42b7-802b-ad304a757022', '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000',
   #'', '2024-05-17T13:44:59.006752', '5bd21f12-e131-4666-aaff-c76fdeefedcf', '00000000-0000-0000-0000-000000000000', False, 
    # '00000000-0000-0000-0000-000000000000', '', '', '', '', '', '34', 'Small', 'Thin', 'Pepperoni, Olives, Mushrooms', '11.3', 'Ordered'] 
  def refresh_data_grid(self):
      try:
          # Fetch the current data from the server
          self.repeating_panel_1.items = anvil.server.call('get_pizza') # Explicitly refresh the DataGrid
  
      #except anvil.server.CallableError as e:
      # Handle error if the server function call fails
      except anvil.server.ExternalError as e:
        print(f"Error while refreshing the grid: {e}")
          


  def refresh_button_click(self, **event_args):
    """This method is called when the REFRESH button is clicked"""
    self.repeating_panel_1.items = anvil.server.call('get_pizza')
    pass
  
