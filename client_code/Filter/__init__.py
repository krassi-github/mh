from datetime import datetime, date as _date
from ._anvil_designer import FilterTemplate
from anvil import *
import anvil.server
from .. import Data

class Filter(FilterTemplate):
  # for binding !!! item = {"from_date": Data.time_from, "to_date": Data.time_to}
  
  def __init__(self, **properties):
    self.init_components(**properties)
    # Data initializing (because this code runs first)
    # GPT rework 20-06-2025
    self.main_form = None  # ще бъде зададен по-късно
    
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
    if not Data.current_zone:
      self.default_zone(0)

    self.set_cur_date()  
    self.all.checked = False
    Data.all = self.all.checked
    
    self.drop_down_1.items = Data.zone_items
    self.flow_panel_2.width = "95%"
    self.flow_panel_1.width = "95%"
    self.t_from.width = "80%"
    self.t_to.width = "80%"
    self.drop_down_1.width = "80%"
    self.drop_down_2.width = "80%"
    self.slice_time.width = "80%"

  #  GPT 19-09-2025 and 20-06-2025
  def to_date_only(self, x):
    if isinstance(x, _date) and not isinstance(x, datetime):
      return x                          # already a date
    if isinstance(x, datetime):
      return x.date()                   # datetime -> date
    if isinstance(x, (int, float)):
      return datetime.fromtimestamp(x).date()  # Unix ts -> date
    if isinstance(x, str):
      # вземи само датната част, смени /->-, парсни като YYYY-MM-DD
      s = x.split()[0].replace('/', '-')
      return datetime.strptime(s, '%Y-%m-%d').date()
    raise ValueError(f'Unsupported date value: {x!r}')

  
  def set_cur_date(self):
    p, d = anvil.server.call("get_first_date")
    p1, d1 = anvil.server.call("get_last_date")
    
    if p or p1:
      self.msg.text +=  f"first or last date {p}  {p1}" 
      self.msg.foreground = "red"
    else:  
      d_date  = self.to_date_only(d)
      d1_date = self.to_date_only(d1)  
      self.cur_date.min_date = d_date
      self.cur_date.max_date = d1_date
    self.cur_date.date = self.to_date_only(Data.current_date) if Data.current_date else d1_date
    # print("Filter says self.cur_date.date =", repr(self.cur_date.date), type(self.cur_date.date))
    
    
  def restore_range_selection(self):
    rng = Data.current_range or "d"

    if rng == "d":
      self.d.selected = True
      self.d_clicked()
    elif rng == "w":
      self.w.selected = True
      self.w_clicked()
    elif rng == "m":
      self.m.selected = True
      self.m_clicked()
    elif rng == "m3":
      self.m3.selected = True
      self.m3_clicked()
    elif rng == "r":
      self.r.selected = True
      self.r_clicked()
    elif rng == "h0":
      self.h0.selected = True
      self.h0_clicked()
    else:
      self.d.selected = True
      Data.current_range = "d"
      
#  GPT 20-06-2025
  def set_main_form(self, main_form):
    self.main_form = main_form
    self.restore_range_selection()

   
  def default_zone(self, zone_index):
    zone = Data.zone_items[zone_index][1]
    self.drop_down_1.selected_value = zone
    Data.set_zone(zone)

# Ranges processing  -------------------------------------------------------------------
  def show_range(self, user, rng, Tb=None, Te=None, Step=None):
    Data.current_range = rng
    #self.parent.parent.render_data(user, rng, Tb=Tb, Te=Te, Step=Step)
    if self.main_form:
      self.main_form.render_data(user, rng, Tb=Tb, Te=Te, Step=Step)
   
  def r_clicked(self, **event_args):        # Range
    if Data.time_from >= Data.time_to or not Data.time_from or not Data.time_to:
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

  def h0_clicked(self, **event_args):
    Data.step = -1


  # Range time_frame  -------------------------------------------------------------------------- 
  def t_from_change(self, **event_args):
    dt = self.item["from_date"].strftime("%Y/%m/%d %H:%M")[:-5] + "23:59"
    if not dt or (Data.time_from >= Data.time_to):
      pass
    else:
      Data.time_from = dt
    if self.r.selected:
      self.show_range("1001", 'r', Tb=Data.time_from, Te=Data.time_to)

  def t_to_change(self, **event_args):
    dt = self.item["to_date"].strftime("%Y/%m/%d %H:%M")[:-5] + "23:59"
    if not dt or (Data.time_from >= Data.time_to):
      pass
    else:
      Data.time_to = dt
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
    
# Events handlers ----------------------------------------------------------
  def cur_date_change(self, **event_args):    # 20-06-2025
    cd = (str(self.cur_date.date)).replace('-', '/') + " 00:00"
    ld = anvil.server.call("get_last_date")
    Data.current_date = cd if cd != ld else ''    # ????? Защо празен стринг
    self.show_range("1001", Data.current_range)
    
  def drop_down_1_change(self, **event_args):
    Data.set_zone(self.drop_down_1.selected_value)
    self.msg.text = self.drop_down_1.selected_value
    self.zone_change()

  def drop_down_2_change(self, **event_args):
    Data.set_zone(self.drop_down_2.selected_value)
    self.msg.text = self.drop_down_2.selected_value
    self.zone_change()

  def slice_time_show(self, **event_args):
    if self.slice_time.selected_value  != "None":
      Data.slice_step = int(self.slice_time.selected_value)
      Data.slice_mode = True
    else:
      Data.slice_step = 0
      Data.slice_mode = False

  def slice_time_change(self, **event_args):
    self.slice_time_show(**event_args)
    # print(f"slice.time_change()  ==>  {Data.slice_mode}   {Data.slice_step}")
    self.zone_change()
