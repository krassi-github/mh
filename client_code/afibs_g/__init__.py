from ._anvil_designer import afibs_gTemplate
from anvil import *
import anvil.server
from .. import Data

class afibs_g(afibs_gTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.repeating_panel_1.items = Data.afibs
    print("afibs_g __init__()")
