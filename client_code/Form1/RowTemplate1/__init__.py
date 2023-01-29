from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server

class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if int(self.lb_2.text) >= 135:
      self.lb_2.foreground = "red"
    if int(self.lb_3.text) >= 85:
      self.lb_3.foreground = "red"
    if int(self.lb_5.text) > 100:
      self.lb_5.foreground = "red"

