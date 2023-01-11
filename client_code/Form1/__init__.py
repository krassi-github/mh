from ._anvil_designer import Form1Template
from anvil import *
import plotly.graph_objects as go
# from . import Data


class Form1(Form1Template):
  bp_sys = [142, 135, 134, 122, 138, 118]
  bp_dia = {90, 85, 85, 78, 82, 75}
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
