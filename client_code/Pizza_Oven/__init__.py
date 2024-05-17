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

        print (record_type, record_id, link_id, time, account, size, crust, toppings, price, status)  # QC check
    
      
      
      
 #['500001.00', 0, '67fd1474-a823-42b7-802b-ad304a757022', '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000',
   #'', '2024-05-17T13:44:59.006752', '5bd21f12-e131-4666-aaff-c76fdeefedcf', '00000000-0000-0000-0000-000000000000', False, 
    # '00000000-0000-0000-0000-000000000000', '', '', '', '', '', '34', 'Small', 'Thin', 'Pepperoni, Olives, Mushrooms', '11.3', 'Ordered'] 
    # print("Tick")
    try:
      record_type = self.subscriber_task.get_state()["recordType"]
      if record_type != '':
        print(f'Record Type -> {record_type}')
        session_id = self.subscriber_task.get_state()["session"]
        if session_id != self.last_session_id:
          print(f"1 Session Id: {session_id}")
          anvil.server.call('set_session_id', session_id)
          records = self.subscriber_task.get_state()["records"]
          print(f"Record Type: {record_type}")
          print(f"Records List: {records}")
          for record in records:
            record_type = record['recordType']
            metadata = record['metadata']
            payload = record['payload']
            item = {'record_type': record_type, 'metadata': metadata, 'payload': payload,}
            self.dg_items.append(item)
            print(f'Item Count: {len(self.dg_items)}')
            
          self.repeating_panel_1.items = self.dg_items
#          self.repeating_panel_1.items = self.repeating_panel_1.items
          
          self.last_session_id = session_id
          
    except Exception as ex:
      print(f'Exception: {repr(ex)}')
      pass
    
    pass
  
