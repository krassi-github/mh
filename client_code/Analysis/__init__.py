from ._anvil_designer import AnalysisTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
from .. import Data
from ..afibs_g import afibs_g


class Analysis(AnalysisTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens
    self.column_panel_L.row_spacing = 4
    self.column_panel_R.row_spacing = 4
    #Data.number, Data.uom, Data.step, Data.Tb1, Data.Tb2
    #self.data_render("1001")
    
  def data_render(self, object):
    #print(f"n= {Data.number} uom= {Data.uom}, s= {Data.step} Tb1= {Data.Tb1} Tb2= {Data.Tb2}")
    r = Data.set_comp_list(object, Data.number, Data.uom, Data.step, Data.Tb1, Data.Tb2)
    r1 = Data.set_comp_summary(object, Data.number, Data.uom, Data.step, Data.Tb1, Data.Tb2)
    # r = Data.set_comp_list("1001", 2, 'm', 360*4, "2023/06/01 00:00", "2023/08/01 00:00")
    # r1 = Data.set_comp_summary("1001", 2, 'm', 360*4, "2023/06/01 00:00", "2023/08/01 00:00")
    if r or r1:
      self.label_R.text = f"No Data {r}   { r1}"
      self.label_R.foreground = "red"
    else:
      self.repeating_panel_1.items = Data.comp_list
      self.repeating_panel_2.items = Data.comp_summary
      self.ser_1.text = "Ser 1: " + Data.Tb1[:10] + " - " + Data.Te1[:10]
      self.ser_2.text = "Ser 2: " + Data.Tb2[:10] + " - " + Data.Te2[:10]
      self.step_v.text = Data.step
      self.t_zone.text = Data.zt_beg + " - " + Data.zt_end
      #print(f"data_render()  ==> Analysis RP items= {self.repeating_panel_1.items}")

  def back_click(self, **event_args):
    open_form('Form1')

