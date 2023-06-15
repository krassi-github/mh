from ._anvil_designer import afib_gridTemplate
from anvil import *
import anvil.server
from .. import Data

class afib_grid(afib_gridTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.repeating_panel_1.items = Data.afibs
