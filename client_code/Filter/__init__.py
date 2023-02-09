from ._anvil_designer import FilterTemplate
from anvil import *
import anvil.server
from .. import Data

class Filter(FilterTemplate):
  # for binding !!! item = {"from_date": Data.time_from, "to_date": Data.time_to}
  
  def __init__(self, **properties):
    p = Data.load_params()
    if p:
      self.parent.parent.label_1.text += f" load_params= {p}"
      self.parent.parent.label_1.foreground = "red" 
    self.item = {"from_date": Data.time_from[:10], "to_date": Data.time_to[:10]}
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.flow_panel_2.width = "95%"
    self.flow_panel_1.width = "95%"
    self.t_from.width = "80%"
    self.t_to.width = "80%"
    self.drop_down_1.width = "80%"
    # Any code you write here will run before the form opens.    
    self.to = self.item.get("to_date", "Error")
    # print(f"Filter says  {self.to}")
   
  def show_range(self, user, rng, Tb=None, Te=None, Step=None):    
    Data.set_bp_list(user, fr=rng)
    Data.set_summary(user, fr=rng)
    self.parent.parent.repeating_panel_1.items = Data.bp_list
    self.parent.parent.show_summary()
    self.parent.parent.plot_1_show()
    
  def d_clicked(self, **event_args):
    self.show_range("1001", 'd')    

  def w_clicked(self, **event_args):
    self.show_range("1001", 'w')    

  def m_clicked(self, **event_args):
    self.show_range("1001", 'm')

  def m3_clicked(self, **event_args):
    self.show_range("1001"", 'm3')  

  def r_clicked(self, **event_args):
    if Data.time_from >= Data.time_to:
      a = alert(f"Time FROM is INVALID\n {Data.time_from} >= {Data.time_to}\
      \n Do you want to correct date(s)?")
      if not c:
        self.r.selected = False
        return()
    else:
      self.show_range("1001", 'r', Tb=Data.time_from, Te=Data.time_to)
#################
  def t_from_change(self, **event_args):
    Data.time_from = self.item["from_date"]
    self.parent.parent.label_2.text += f" {Data.time_from}"

  def t_to_change(self, **event_args):
    Data.time_to = self.item["to_date"]
    self.parent.parent.label_2.text += f" TO {Data.time_to}"









