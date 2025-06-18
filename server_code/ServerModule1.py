import anvil.server
# Във Server Module (например 'ServerModule1')

import plotly.graph_objects as go
from plotly.subplots import make_subplots

@anvil.server.callable
def get_afib_figure():
  # Примерни фиктивни данни
  yearly_data = {
    2021: {1: 0, 2: 1, 3: 0, 1: 2, 5: 0, 6: 0, 7: 1, 8: 2, 9: 3, 10: 0, 11: 2, 12: 0},
    2022: {1: 0, 2: 1, 3: 0, 2: 2, 5: 0, 6: 0, 7: 1, 8: 2, 9: 3, 10: 0, 11: 2, 12: 0},
    2023: {1: 0, 2: 1, 3: 0, 3: 2, 5: 0, 6: 0, 7: 1, 8: 2, 9: 3, 10: 0, 11: 2, 12: 0}
  }

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
        marker_color=["crimson" if y > 0 else "lightgrey" for y in y_vals],
        showlegend=False
      ),
      row=i+1, col=1
    )
    fig.update_xaxes(
      tickmode='array',
      tickvals=list(range(1, 13)),
      #ticktext=["Ян", "Фев", "Март", "Апр", "Май", "Юни",
      #          "Юли", "Авг", "Сеп", "Окт", "Ное", "Дек"], '''      
      ticktext = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
      tickangle=0,  # ← ето това завърта етикетите; -45 OR -90
      row=i+1,
      col=1
    )


  fig.update_layout(
    height=300 * len(yearly_data),
    title="AFIB събития по месеци и години",
    margin=dict(t=40, b=20),
    xaxis=dict(
      tickmode='array',
      tickvals=list(range(1, 13)),
      ticktext=["Ян", "Фев", "Март", "Апр", "Май", "Юни",
                "Юли", "Авг", "Сеп", "Окт", "Ное", "Дек"]
    )
  )

  return fig

#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
