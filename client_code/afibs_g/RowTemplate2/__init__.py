from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server
from ... import Data

class RowTemplate2(RowTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)    
