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
 
#    The basic form is how to create a list of colors for the x-axis, so there are many different approaches. 
# I suggest this as an example of how to make a color list with conditions.
'''  
  # sample df
  df = pd.DataFrame({'Date': ['2010 - Q3','2010 - Q4','2011 - Q1','2011 - Q2','2011 - Q3','2011 - Q4'],
                    'Rate' : ['11.4','12.2','14.4','15.5','10.1','13.1'],
                    'Rate1': ['2.1','2.3','1.9','1.6','2.5','1.1']
                  })
  
  clrs = []
  for i in range(len(df)):
      if df.loc[i,'Date'][:4] == '2010':
          clrs.append('rgb(222,0,0)')
      else:
          clrs.append('rgb(0,100,0)')
  #clrs = ['rgb(222,0,0)','rgb(222,0,0)','rgb(0,100,0)','rgb(0,100,0)','rgb(0,100,0)','rgb(0,100,0)']
  
  fig = go.Figure(
              data=[
                    go.Bar(
                          x=df['Date'],
                          y=df['Rate'],
                          name='Natural Level'
                          ),
                    go.Bar(
                          x=df['Date'],
                          y=df['Rate1'],
                          name='Change',
                          marker=dict(color=clrs)
                          )
                    ],
              layout=go.Layout(
                  title='Measuring excess demand and supply in the market.',
                  xaxis=dict(
                      tickangle=90,
                      tickfont=dict(family='Rockwell', color='crimson', size=14)
                  ),
                  yaxis=dict(
                      title='Rate',
                      showticklabels=True
                  ),
                  barmode='stack',
              )
          )
  
  fig.show()
'''
