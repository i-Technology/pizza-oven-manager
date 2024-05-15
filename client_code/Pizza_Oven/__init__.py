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
    
    # print("Launching Subscriber!")    
    # self.subscriber_task = anvil.server.call('launch_subscriber_task')

    print("Starting Timer")
    self.timer_1.interval = 1
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
    if message != 'None':
      print(message)
  
    # print("Tick")
#     try:
#       record_type = self.subscriber_task.get_state()["recordType"]
#       if record_type != '':
#         print(f'Record Type -> {record_type}')
#         session_id = self.subscriber_task.get_state()["session"]
#         if session_id != self.last_session_id:
#           print(f"1 Session Id: {session_id}")
#           anvil.server.call('set_session_id', session_id)
#           records = self.subscriber_task.get_state()["records"]
#           print(f"Record Type: {record_type}")
#           print(f"Records List: {records}")
#           for record in records:
#             record_type = record['recordType']
#             metadata = record['metadata']
#             payload = record['payload']
#             item = {'record_type': record_type, 'metadata': metadata, 'payload': payload,}
#             self.dg_items.append(item)
#             print(f'Item Count: {len(self.dg_items)}')
            
#           self.repeating_panel_1.items = self.dg_items
# #          self.repeating_panel_1.items = self.repeating_panel_1.items
          
#           self.last_session_id = session_id
          
#     except Exception as ex:
#       print(f'Exception: {repr(ex)}')
#       pass
    
    pass
  
