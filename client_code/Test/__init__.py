from ._anvil_designer import TestTemplate
from anvil import *
import plotly.graph_objects as go

class Test(TestTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)


    data = {
        "original":[15, 23, 32, 10, 23],
        "model_1": [4,   8, 18,  6,  0],
        "model_2": [11, 18, 18,  0,  20],
        "labels": [
            "feature",
            "question",
            "bug",
            "documentation",
            "maintenance"
        ]
    }
    
    fig3 = go.Figure(
        data=[
            go.Bar(
                name="Original",
                x=data["labels"],
                y=data["original"],
                offsetgroup=0,
            ),
            go.Bar(
                name="Model 1",
                x=data["labels"],
                y=data["model_1"],
                offsetgroup=1,
                marker = dict(color = "white", )
            ),
            go.Bar(
                name="Model 2",
                x=data["labels"],
                y=data["model_2"],
                offsetgroup=1,
                base=data["model_1"], 
            )
        ],
        layout=go.Layout(
            title="Issue Types - Original and Models",
            yaxis_title="Number of Issues"
        )
    )
    # !!! GO through "figure"
    self.plot_1.figure = fig3
