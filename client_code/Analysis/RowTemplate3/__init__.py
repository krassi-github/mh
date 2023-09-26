from ._anvil_designer import RowTemplate3Template
from anvil import *
import anvil.server
from .. import Data
from ... afibs_g import afibs_g
import time

r = 0  # global r
class RowTemplate3(RowTemplate3Template):
  def __init__(self, **properties):
    global r
    print("RowTemplate3 ///////////////////////////////////////")
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.row_spacing = 0
    # Test of assignment instead of binding
    self.s1.text = self.item['s1']
    self.s2.text = self.item["s2"]
    self.d1.text = self.item["d1"]
    self.d2.text = self.item["d2"]
    self.m1.text = self.item["m1"]
    self.m2.text = self.item["m2"]
    print(f"s1 label text= {self.s1.text}")
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
    
    if not r%2:
      pass
      self.color_rows()
    r += 1  

  def color_rows(self):
    #print(self.get_components())
    #return()
    self.no.background = "rgba(103, 80, 164, 0.05)"      #"rgba(69,183,249,0.1)"  #'theme:Gray 200'
    self.s1.background = "rgba(103, 80, 164, 0.05)"      #"rgba(69,183,249,0.1)"
    self.s2.background = "rgba(103, 80, 164, 0.05)"      #"rgba(69,183,249,0.1)"
    self.d1.background = "rgba(103, 80, 164, 0.05)"      #"rgba(69,183,249,0.1)"
    self.d2.background = "rgba(103, 80, 164, 0.05)"      #"rgba(69,183,249,0.1)"
    self.p1.background = "rgba(103, 80, 164, 0.05)"      #"rgba(69,183,249,0.1)"  #'theme:Gray 200'
    self.p2.background = "rgba(103, 80, 164, 0.05)"      #"rgba(69,183,249,0.1)"
    self.m1.background = "rgba(103, 80, 164, 0.05)"      #"rgba(69,183,249,0.1)"
    self.m2.background = "rgba(103, 80, 164, 0.05)"      #"rgba(69,183,249,0.1)"
    self.a1.background = "rgba(0, 0, 0, 0.0)"            #"rg
    self.a2.background = "rgba(0, 0, 0, 0.0)" 

  def L1_click(self, **event_args):
    afib_print = ""
    
    afibs = Data.afib_details(self.link_1.tag)   
    if type(afibs) == type("str"):
      afib_print = str(afibs)
      alert(content=f"{self.link_1.tag}    {afib_print}", large=True, title="AFIB Details")
    else:
      alert(afibs_g(), large=True, title="AFIB Details")
      # alert(content=f"{self.link_1.tag}\n{afib_print}", large=True, title="AFIB Details")

  def L2_click(self, **event_args):
    afib_print = ""


'''    self.parent.parent.repeating_panel_1.items = Data.comp_list
    print(f"RT_3 self.item= {self.item}  ")
    print(f"item['s1']=  {self.item['s1']}")
    self.s1.text = self.item['s1']
    self.s2.text = self.item["s2"]
    self.d1.text = self.item["d1"]
    self.d2.text = self.item["d2"]
    self.m1.text = self.item["m1"]
    self.m2.text = self.item["m2"]'''