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
    self.countdown=0    # baking timer
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the BAKE button is clicked"""
    self.item.update(status='Baking')
    self.refresh_data_bindings()
    self.timer_1.interval=30
    self.countdown = 2
    pass

  def button_2_click(self, **event_args):
    """This method is called when the BOX button is clicked"""
    self.item.update(status='Boxing')
    self.refresh_data_bindings()
    pass

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.countdown -= 1
    if self.countdown == 0:
      self.row_color = Red
    print (self.timer_1)
    pass



