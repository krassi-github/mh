from ._anvil_designer import FilterTemplate
from anvil import *
import anvil.server
from . import Data

class Filter(FilterTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def d_clicked(self, **event_args):
    Data.show_range("1001", 'd')    

  def w_clicked(self, **event_args):
    Data.show_range("1001", 'w')    

  def m_clicked(self, **event_args):
    Data.show_range("1001", 'm')

  def m3_clicked(self, **event_args):
    Data.show_range("1001"", 'm3')

  def range_clicked(self, **event_args):
    
    pass

