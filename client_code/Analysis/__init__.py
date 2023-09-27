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
    self.data_render()
    
  def data_render(self):
    r = Data.set_comp_list("1001", 2, 'd', 360, "2023/08/01 00:00", "2023/08/11 00:00")
    self.repeating_panel_1.items = Data.comp_list
    print(f"data_render()  ==> Analysis RP items= {self.repeating_panel_1.items}")

  def back_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Form1')

