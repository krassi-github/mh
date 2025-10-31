from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
from .. import Data
from ... afibs_g import afibs_g
from .. import Form1

r = 0; run = 0
class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    global r
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #save the date;
    if Data.slice_mode:
      print(f"RT item= {self.item} ")
      i = self.item["i"] 
      self.link_1.tag = Data.afibs_dt_cnt[i].get("dt")
      self.slice_window = self.item["date"]
    else:
      self.link_1.tag = self.lb_1.text
      self.slice_window = "00:00 - 23:59"

    self.lb_1.text = self.item["date"] if Data.current_range in ["d", "w"] \
    or Data.slice_mode is True else self.item["date"][:10]  # 20/09/2025, 09/10/2025
    self.row_spacing = 0
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
      pass
      self.color_rows()
    r += 1; run  

  def color_rows(self):
    #print(self.get_components())
    #return()
    self.lb_1.background = "rgba(103, 80, 164, 0.05)"      #"rgba(69,183,249,0.1)"  #'theme:Gray 200'
    self.lb_2.background = "rgba(103, 80, 164, 0.05)"      #"rgba(69,183,249,0.1)"
    self.lb_3.background = "rgba(103, 80, 164, 0.05)"      #"rgba(69,183,249,0.1)"
    self.lb_4.background = "rgba(103, 80, 164, 0.05)"      #"rgba(69,183,249,0.1)"
    self.lb_5.background = "rgba(103, 80, 164, 0.05)"      #"rgba(69,183,249,0.1)"
    self.lb_6.background = "rgba(0, 0, 0, 0.0)"            #"rgba(69,183,249,0.1)"


  def link_1_click(self, **event_args):
    # ако искаш да забраниш детайли в slice режим:
    # if Data.slice_mode:
    #   return
    get_open_form().label_2.text += self.link_1.tag + ' '    
    rows, msg = Data.afib_details(self.link_1.tag, slice_window=self.slice_window)
  
    if not rows:
      alert(content=f"{self.link_1.tag}\n{msg}", large=False, title="AFIB Details")
      return
    alert(afibs_g(rows), large=True, title="AFIB Details")

# Old or alternatives
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
