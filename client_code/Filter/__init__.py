from ._anvil_designer import FilterTemplate
from anvil import *
import anvil.server
from .. import Data

class Filter(FilterTemplate):
  # for binding !!! item = {"from_date": Data.time_from, "to_date": Data.time_to}
  
  def __init__(self, **properties):
    self.init_components(**properties)
    # Data initializing (because this code runs first)
    p = Data.load_params()
    if p:
      self.msg.text += f" load_params= {p}"
      self.msg.foreground = "red" 
    p = Data.load_sysdata()
    if p:
      self.msg.text +=  f" load_sysdata= {p}"
      self.msg.foreground = "red" 
    p = Data.load_zones()
    if p:
      self.msg.text +=  f" load_zones= {p}" 
      self.msg.foreground = "red"
    #input("Check and GO ")
    self.item = {"from_date": Data.time_from[:10], "to_date": Data.time_to[:10]}
    self.drop_down_1.items = Data.zone_items
    self.drop_down_2.items = Data.custom_zone_items

    '''    TO BE TESTED
    self.drop_down_2.include_placeholder = True
    self.drop_down_2.placeholder = "Select a custom zone"
    self.drop_down_2.selected_value = None
    self.drop_down_2.items = self.drop_down_2.items
    '''
    self.default_zone(0)
    #self.msg.text = Data.current_zone+' '+Data.zt_beg+' '+Data.zt_end
    # Set Form properties and Data Bindings.
    
    self.d.selected = True
    Data.current_range = 'd'
    self.all.checked = False
    Data.all = self.all.checked
    self.drop_down_1.items = Data.zone_items
    self.flow_panel_2.width = "95%"
    self.flow_panel_1.width = "95%"
    self.t_from.width = "80%"
    self.t_to.width = "80%"
    self.drop_down_1.width = "80%"
    self.drop_down_2.width = "80%"
    # Any code you write here will run before the form opens.
    #self.fr = self.item.get("from_date", "Error")
    #self.to = self.item.get("to_date", "Error")  


  def default_zone(self, zone_index):
    zone = Data.zone_items[zone_index][1]
    self.drop_down_1.selected_value = zone
    Data.set_zone(zone)


# Ranges processing  -------------------------------------------------------------------
  def show_range(self, user, rng, Tb=None, Te=None, Step=None):
    Data.current_range = rng
    self.parent.parent.render_data(user, rng, Tb=Tb, Te=Te, Step=Step)
   
  def r_clicked(self, **event_args):        # Range
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
    self.show_range("1001", 'm3')


  # Range time_frame  -------------------------------------------------------------------------- 
  def t_from_change(self, **event_args):
    Data.time_from = self.item["from_date"].strftime("%Y/%m/%d %H:%M")
    if self.r.selected:
      self.show_range("1001", 'r', Tb=Data.time_from, Te=Data.time_to)

  def t_to_change(self, **event_args):
    Data.time_to = self.item["to_date"].strftime("%Y/%m/%d %H:%M")[:-5] + "23:59"    
    if self.r.selected:
      self.show_range("1001", 'r', Tb=Data.time_from, Te=Data.time_to)
      
  # Standard/Custome zone ---------------------------------------------------------------------
  def zone_change(self, **event_args):
    Data.all = self.all.checked
    '''
    Tb = Te = None
    if Data.current_range == 'r':
      Tb=Data.loaded_from        #time_from
      Te=Data.loaded_to          # time_to
      '''
    Tb=Data.loaded_from        #time_from
    Te=Data.loaded_to          # time_to
    print(f"zone_change() ==> loaded_from {Data.loaded_from}   loaded_to {Data.loaded_to}")
    self.show_range("1001", Data.current_range, Tb=Tb, Te=Te)
    

  def drop_down_1_change(self, **event_args):
    Data.set_zone(self.drop_down_1.selected_value)
    self.msg.text = self.drop_down_1.selected_value
    self.zone_change()

  def drop_down_2_change(self, **event_args):
    Data.set_zone(self.drop_down_2.selected_value)
    self.msg.text = self.drop_down_2.selected_value
    self.zone_change()
