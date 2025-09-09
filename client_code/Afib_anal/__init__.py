from ._anvil_designer import Afib_analTemplate
from anvil import *
import anvil.server

import plotly.graph_objects as go
#from plotly.subplots import make_subplots
from .. import Data


class Afib_anal(Afib_analTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.show_plot()
    self.show_grid()


  # Във форма Afib_anal, метод или бутон
  def show_plot(self, **event_args):
    fig = anvil.server.call('get_afib_figure')
    self.column_panel_2.clear()
    self.column_panel_2.add_component(Plot(figure=fig))

  def show_grid(self):
    # self.repeating_panel_1.items = list(filter(lambda row: row.get("afib"), Data.bp_list))
    self.repeating_panel_1.items = [row for row in Data.bp_list if row.get("afib") is not None and row.get("afib") != ""]

