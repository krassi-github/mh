from ._anvil_designer import FilterTemplate
from anvil import *
import anvil.server

class Filter(FilterTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def d_clicked(self, **event_args):
    Data.show_range('d')    

  def w_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    pass

  def m_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    pass

  def m3_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    pass

  def range_clicked(self, **event_args):
    
    pass

