from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
from .. import Data

r = 0
class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    global r
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if int(self.lb_2.text) >= Data.params["red_sys"]:
      self.lb_2.foreground = "red"
    elif int(self.lb_2.text) >= Data.params["orange_sys"]:
      self.lb_2.foreground = "orange"
    if int(self.lb_3.text) >= Data.params["red_dia"]:
      self.lb_3.foreground = "red"
    elif  int(self.lb_3.text) >= Data.params["orange_dia"]:
      self.lb_3.foreground = "orange"
    if int(self.lb_5.text) > Data.params["red_mean"]:
      self.lb_5.foreground = "red"
    if (self.lb_6.text):
      self.lb_6.foreground = "red"    
    if not r%2:
      self.color_rows()
    r += 1
    #print(f"r= {r}")

  def color_rows(self):
    #print(self.get_components())
    return()
    self.lb_1.background = "rgba(69,183,249,0.1)"  #'theme:Gray 200'
    self.lb_2.background = "rgba(69,183,249,0.1)"
    self.lb_3.background = "rgba(69,183,249,0.1)"
    self.lb_4.background = "rgba(69,183,249,0.1)"
    self.lb_5.background = "rgba(69,183,249,0.1)"
    self.lb_6.background = "rgba(69,183,249,0.1)"
  '''
  def color_rows(self):
    print(self.get_components())
    for i, r in enumerate(self.get_components()):
      if not i%2:
        self.lb_1.background = "rgba(69,183,249,0.1)"  #'theme:Gray 200'
        self.lb_2.background = "rgba(69,183,249,0.1)"
        self.lb_3.background = "rgba(69,183,249,0.1)"
        self.lb_4.background = "rgba(69,183,249,0.1)"
        self.lb_5.background = "rgba(69,183,249,0.1)"
        self.lb_6.background = "rgba(69,183,249,0.1)"
  '''
      

