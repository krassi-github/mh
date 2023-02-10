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
    self.all.checked = False
    Data.all = self.all.checked
    self.flow_panel_2.width = "95%"
    self.flow_panel_1.width = "95%"
    self.t_from.width = "80%"
    self.t_to.width = "80%"
    self.drop_down_1.width = "80%"
    # Any code you write here will run before the form opens.
    self.fr = self.item.get("from_date", "Error")
    self.to = self.item.get("to_date", "Error")  

  def t_from_change(self, **event_args):
    Data.time_from = self.item["from_date"].strftime("%Y/%m/%d %H:%M")
    if self.r.selected:
      self.show_range("1001", 'r', Tb=Data.time_from, Te=Data.time_to)

  def t_to_change(self, **event_args):
    Data.time_to = self.item["to_date"].strftime("%Y/%m/%d %H:%M")[:-5] + "23:59"    
    if self.r.selected:
      self.show_range("1001", 'r', Tb=Data.time_from, Te=Data.time_to)

# Ranges processing
  def show_range(self, user, rng, Tb=None, Te=None, Step=None):    
    r = Data.set_bp_list(user, fr=rng, Tb=Tb, Te=Te, Step=Step)
    if r:
      self.parent.parent.label_2.text += f"  set_bp_list= {r}"
      self.parent.parent.label_2.foreground = "red"
    r = Data.set_summary(user, fr=rng, Tb=Tb, Te=Te)
    if r:
      self.label_2.text += f"  set_summary= {r} "
      self.label_2.foreground = "red"
    self.parent.parent.repeating_panel_1.items = Data.bp_list
    self.parent.parent.show_summary()
    self.parent.parent.plot_1_show()
   
  def r_clicked(self, **event_args):
    if Data.time_from >= Data.time_to:
      a = alert(f"Time FROM is INVALID\n {Data.time_from} >= {Data.time_to}\
      \n Do you want to correct date(s)?")
      if not a:
        self.r.selected = False
        return()
    else:
      self.show_range("1001", 'r', Tb=Data.time_from, Te=Data.time_to)
          
  def d_clicked(self, **event_args):
    self.show_range("1001", 'd')    

  def w_clicked(self, **event_args):
    self.show_range("1001", 'w')    

  def m_clicked(self, **event_args):
    self.show_range("1001", 'm')

  def m3_clicked(self, **event_args):
    self.show_range("1001"", 'm3')

  def all_change(self, **event_args):
    Tb = Te = None
    Data.all = self.all.checked
    if Data.current_range == 'r':
      Tb=Data.time_from
      Te=Data.time_to
    self.show_range("1001", Data.current_range, Tb=Tb, Te=Te)

 