from ._anvil_designer import FilterTemplate
from anvil import *
import anvil.server
from .. import Data

class Filter(FilterTemplate):
  # for binding
  item = {"from_date": Data.time_from, "to_date": Data.time_to}
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)    
    # Any code you write here will run before the form opens.

  def show_range(self, user, rng):    
    Data.set_bp_list(user, fr=rng)
    Data.set_summary(user, fr=rng)
    self.parent.parent.repeating_panel_1.items = Data.bp_list
    self.parent.parent.show_summary()
    self.parent.parent.plot_1_show()
    
  def d_clicked(self, **event_args):
    self.show_range("1001", 'd')    

  def w_clicked(self, **event_args):
    self.show_range("1001", 'w')    

  def m_clicked(self, **event_args):
    self.show_range("1001", 'm')

  def m3_clicked(self, **event_args):
    self.show_range("1001"", 'm3')

  def range_clicked(self, **event_args):    
    pass

  def t_from_change(self, **event_args):
    Data.time_from = self.item["from_date"]
    self.parent.parent.label_2.text += f" {Data.time_from}"

  def t_to_change(self, **event_args):
    Data.time_to = self.item["to_date"]
    self.parent.parent.label_2.text += f" TO {Data.time_to}"




