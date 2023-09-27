from ._anvil_designer import RowTemplate5Template
from anvil import *
import anvil.server
from .. import Data

class RowTemplate5(RowTemplate5Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.row_spacing = 0
    # print(f"Data.comp_summary  {Data.comp_summary}")
    print(f" Locally  {self.item}")
    self.no.text = self.item["no"]
    self.s1.text = self.item['s1']
    self.s2.text = self.item["s2"]
    self.d1.text = self.item["d1"]
    self.d2.text = self.item["d2"]
    self.p1.text = self.item["p1"]
    self.p2.text = self.item["p2"]
    self.m1.text = self.item["m1"]
    self.m2.text = self.item["m2"]
    self.a1.text = self.item["a1"]
    self.a2.text = self.item["a2"]

        # Colorizing  the sys, dia, mean, afib values
    if int(self.s1.text) >= Data.params["red_sys"]:
      self.s1.foreground = "red"
    if int(self.s2.text) >= Data.params["red_sys"]:
      self.s2.foreground = "red"
    elif int(self.s1.text) >= Data.params["orange_sys"]:
      self.s1.foreground = "orange"
    elif int(self.s2.text) >= Data.params["orange_sys"]:      
      self.s2.foreground = "orange"
      
    if int(self.d1.text) >= Data.params["red_sys"]:
      self.s1.foreground = "red"
    if int(self.d2.text) >= Data.params["red_sys"]:
      self.s1.foreground = "red"
    elif int(self.d1.text) >= Data.params["orange_sys"]:
      self.d1.foreground = "orange"
    elif int(self.d2.text) >= Data.params["orange_sys"]:
      self.d2.foreground = "orange"

    if int(self.m1.text) >= Data.params["red_sys"]:
      self.m1.foreground = "red"
    if int(self.m2.text) >= Data.params["red_sys"]:
      self.m1.foreground = "red"
    
    if (self.a1.text):
      self.a1.foreground = "red"
    if (self.a2.text):
      self.a2.foreground = "red"

