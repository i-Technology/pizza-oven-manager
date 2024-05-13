from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.background = "lightblue"  # You can use any CSS color here
    self.countdown=0    # baking timer
    self.item.update(status='Ordered')
    self.status = self.item['status']
    self.refresh_data_bindings()
    self.account = self.item['account_no']
    self.size=self.item['size']
    self.crust=self.item['crust']
    self.toppings=self.item['toppings']
   # self.price=self.item['price']
    
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the BAKE button is clicked"""
    self.item.update(status='Baking')
    self.status = 'Baking'
    self.refresh_data_bindings()
    self.timer_1.interval=1
    self.countdown = 5
    pass

  def button_2_click(self, **event_args):
    """This method is called when the BOX button is clicked"""
    self.item.update(status='Boxing')
    self.status = 'Boxing'
    self.background = "lightgreen"    
    self.refresh_data_bindings()
    pass

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    if self.countdown > 0:
      print (self.countdown)
      
      self.countdown -= 1
      self.timer_label.text = str(self.countdown)
      if self.countdown == 0:
        self.background = "red"
        self.refresh_data_bindings()

    pass

  def button_3_click(self, **event_args):
    """This method is called when the DONE button is clicked"""
    self.item.delete()
    self.remove_from_parent()  
    self.status = 'Delivering'
    anvil.server.call('publish_pizza', 'Update', self.account, self.size, self.crust, self.toppings, self.price,self.status)
    pass




