from ._anvil_designer import Filter_aTemplate
from anvil import *
import anvil.server
from .. import Data

# Class's globals (for internal usage)
tb1 = ""
tb2 = ""
Tb1 = ""
Tb2 = ""

class Filter_a(Filter_aTemplate):
  # for binding !!! item = {"from_date": Data.time_from, "to_date": Data.time_to}

  def __init__(self, **properties):
    self.init_components(**properties)

    #input("Check and GO ")
    # ?? self.item = {"from_date": Data.time_from[:10], "to_date": Data.time_to[:10]}
    self.uom.items = Data.uom_items
    self.drop_down_1.items = Data.zone_items
    self.drop_down_2.items = Data.custom_zone_items

    '''    TO BE TESTED
    self.drop_down_2.include_placeholder = True
    self.drop_down_2.placeholder = "Select a custom zone"
    self.drop_down_2.selected_value = None
    self.drop_down_2.items = self.drop_down_2.items
    '''
    #self.default_zone(0)
    if not Data.step:
      self.d.selected = True
      self.d_clicked()
    self.number.text = 1
    self.flow_panel_2.width = "95%"
    self.flow_panel_1.width = "95%"
    self.period_1.width = "80%"
    self.period_2.width = "80%"
    self.drop_down_1.width = "80%"
    self.drop_down_2.width = "80%"
    # Any code you write here will run before the form opens.
    self.uom_change()
    self.number_change()


  def default_zone(self, zone_index):
    zone = Data.zone_items[zone_index][1]
    self.drop_down_1.selected_value = zone
    Data.set_zone(zone)


# Ranges processing  -------------------------------------------------------------------
  def show_range(self, object):
    self.parent.parent.data_render(object)


# Period parameters setting  ---------------------------------------------------------------
# Period length entry ---------------
  def period_len(self):
    pass
  def uom_change(self, **event_args):
    sv = self.uom.selected_value
    if sv == 'd':
      self.t_unit.text = "d"  # "day"
    elif sv == 'w':
      self.t_unit.text = "w"  # "week"
    else:
      self.t_unit.text = "m"    # "month"
    Data.uom = self.uom.selected_value

  def uom_show(self, **event_args):
    self.uom_change(**event_args)


  def number_change(self, **event_args):
    if not self.number.text:
      # to prevent TypeError: '>' not supported between instances of 'NoneType' and 'int'
      return
    if int(self.number.text) > Data.max_number[0] or int(self.number.text) <= 0:
      alert("The number must be positive integer less than 100. \\nPlease, try again!", title="ERROR message")
      return      
    self.period.text = self.number.text
    Data.number = int(self.number.text)

  def number_pressed_enter(self, **event_args):
    self.number_change()

# Steps selection   --------------- 
  def h2_clicked(self, **event_args):
    Data.step = 2 * 60

  def h6_clicked(self, **event_args):
    Data.step = 6 * 60

  def d_clicked(self, **event_args):
    Data.step = 24 * 60
    # self.show_range("1001", 'd')

  def w_clicked(self, **event_args):
    Data.step = 7 * 24 * 60

  def m_clicked(self, **event_args):
    Data.step = 30 * 24 * 60

  # Special cases:
  # 1) To get raw data records
  def h0_clicked(self, **event_args):
    Data.step = -1
    
  # 2) To get averaged data records
  def ha_clicked(self, **event_args):
    Data.step = -2


# Start points  ----------------
  def periods_verification(self):
    global Tb1, Tb2
    Te1, Te2 = anvil.server.call("periods_calc", Data.number, Data.uom, Data.step, Tb1, Tb2)
    
    
  def period_1_change(self, **event_args):    
    global tb1, Tb1, Tb2
    Tb1 = (str(self.period_1.date)).replace('-', '/') + ' ' + "00:00"
    Te1, dummy = anvil.server.call("periods_calc", Data.number, Data.uom, Data.step, Tb1=Tb1)
    r = anvil.server.call("check_data", "1001", Tb1, Te1)
    if not r:
      alert(f"No DATA in period {Tb1} -- {Te1}", title="WARNING")
    Data.Tb1 = Tb1

  def period_2_change(self, **event_args):
    global tb2, Tb1, Tb2
    Tb2 = (str(self.period_2.date)).replace('-', '/') + ' ' + "00:00"
    dummy, Te2 =  anvil.server.call("periods_calc", Data.number, Data.uom, Data.step, Tb2=Tb2)
    r = anvil.server.call("check_data", "1001", Tb2, Te2)
    if not r:
      alert(f"No DATA in period {Tb2} -- {Te2}", title="WARNING")
    Data.Tb2 = Tb2

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
    self.show_range("1001")    # , Data.current_range, Tb=Tb, Te=Te

  def drop_down_1_change(self, **event_args):
    Data.set_zone(self.drop_down_1.selected_value)
    self.msg.text = self.drop_down_1.selected_value
    self.zone_change()

  def drop_down_2_change(self, **event_args):
    Data.set_zone(self.drop_down_2.selected_value)
    self.msg.text = self.drop_down_2.selected_value
    self.zone_change()

# Start Comparison procedure
  def start_button_click(self, **event_args):
    if Data.Tb1 == "" or Data.Tb2 == "":
      alert("Start times of two periods not available!\n Please CHECK!", title="WARNING")
      return()
    self.parent.parent.data_render("1001")