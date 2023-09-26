from ._anvil_designer import AnalysisTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server

class Analysis(AnalysisTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens
    r = Data.set_comp_list("1001", 2, fr='d', Step=360, Tb1="2023/08/01 00:00", Tb2="2023/08/11 00:00")
    self.repeating_panel_1.items = Data.comp_list
