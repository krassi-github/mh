from ._anvil_designer import Afib_analTemplate
from anvil import *
import anvil.server

import plotly.graph_objects as go
#from plotly.subplots import make_subplots


class Afib_anal(Afib_analTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.show_plot()


  # Във форма Afib_anal, метод или бутон
  def show_plot(self, **event_args):
    fig = anvil.server.call('get_afib_figure')
    self.column_panel_2.clear()
    self.column_panel_2.add_component(Plot(figure=fig))

