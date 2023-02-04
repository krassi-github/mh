from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
from .. import Data

class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if int(self.lb_2.text) >= Data.red_sys:
      self.lb_2.foreground = "red"
    elif int(self.lb_2.text) >= Data.orange_sys:
      self.lb_2.foreground = "orange"
    if int(self.lb_3.text) >= Data.red_dia:
      self.lb_3.foreground = "red"
    elif  int(self.lb_3.text) >= Data.orange_dia:
      self.lb_3.foreground = "orange"
    if int(self.lb_5.text) > Data.red_mean:
      self.lb_5.foreground = "red"
    if (self.lb_5.text):
      self.lb_6.foreground = "red"
      

