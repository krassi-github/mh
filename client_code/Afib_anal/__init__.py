from ._anvil_designer import Afib_analTemplate
from anvil import *
import anvil.server

class Afib_anal(Afib_analTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.


import plotly.graph_objects as go
from plotly.subplots import make_subplots

def load_afib_bargraph(self, yearly_data):
  """
  yearly_data: dict от типа {
    2021: {1: 0, 2: 1, ..., 12: 0},
    2022: {1: 3, ..., 12: 1},
    ...
  }
  """
  from anvil import Plot
  from anvil import PlotComponent

  fig = make_subplots(
    rows=len(yearly_data),
    cols=1,
    shared_xaxes=True,
    subplot_titles=[str(y) for y in yearly_data.keys()]
  )

  for i, (year, months) in enumerate(yearly_data.items()):
    x_vals = list(range(1, 13))
    y_vals = [months.get(m, 0) for m in x_vals]

    fig.add_trace(
      go.Bar(
        x=x_vals,
        y=y_vals,
        name=str(year),
        marker_color=["crimson" if y > 0 else "lightgrey" for y in y_vals],
        showlegend=False
      ),
      row=i+1, col=1
    )

  fig.update_layout(
    height=300 * len(yearly_data),
    title_text="AFIB събития по месеци и години",
    margin=dict(t=40, b=20),
    xaxis=dict(tickmode='array', tickvals=list(range(1, 13)),
               ticktext=["Ян", "Фев", "Март", "Апр", "Май", "Юни", "Юли", "Авг", "Сеп", "Окт", "Ное", "Дек"])
  )

  self.content_panel_1.clear()
  self.content_panel_1.add_component(Plot(fig))
