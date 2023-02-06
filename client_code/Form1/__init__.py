from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import plotly.graph_objects as go
from .. import Data


class Form1(Form1Template):  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    #self.column_panel_2.width = "default"
    #self.b_up.width = "80"
    #self.b_up.text = "   "
    #self.b_dn.width = "60"
    self.column_panel_2.row_spacing = 4
    #self.label_1.text = self.column_panel_2.width
    Data.load_params()
    r = Data.set_bp_list("1001", 'd')
    if r:
      self.label_1.text += f"  set_bp_list= [{r}] "
      print(f"  set_bp_list= {r} ")    
    self.repeating_panel_1.items = Data.bp_list  # 
    self.color_rows(self.repeating_panel_1)
    self.show_summary()
    self.plot_1_show()

  def color_rows(self, rep):
    for i, r in enumerate(rep.get_components()):
      if not i%2:
        r.background = "rgba(69,183,249,0.1)"  #'theme:Gray 200'     


  def show_summary(self):
    self.lb_21.text = Data.bp_list[-2]["date"]
    self.lb_22.text = Data.bp_list[-2]["sys"]
    self.lb_23.text = Data.bp_list[-2]["dia"]
    self.lb_24.text = Data.bp_list[-2]["pul"]
    self.lb_25.text = Data.bp_list[-2]["mean"]
    self.lb_26.text = Data.bp_list[-2]["afib"]
    self.lb_26.foreground = "red"    

    self.lb_31.text = Data.bp_list[-1]["date"]
    self.lb_32.text = Data.bp_list[-1]["sys"]
    self.lb_33.text = Data.bp_list[-1]["dia"]
    self.lb_34.text = Data.bp_list[-1]["pul"]
    self.lb_35.text = Data.bp_list[-1]["mean"]
    self.lb_36.text = Data.bp_list[-1]["afib"]
    self.lb_36.foreground = "red"

  def b_up_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def b_dn_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
  
  def plot_1_show(self):
    fig3 = go.Figure(
      data=[
        go.Bar(
          name="BP-D",
          x=Data.x_data,
          y=Data.bp_dia,
          offsetgroup=0,
          marker = dict(color = "rgba(10, 10, 10, 0.05)", )
        ),
        go.Bar(
          name="BP-S",
          x=Data.x_data,
          y=Data.bp_sys_add,
          offsetgroup=0,
          base = Data.bp_dia,          
          marker = dict(color=Data.bp_colors, )      # dict(color = self.clrs, )
        ),
        go.Scatter(
          name="BP-M",
          x=Data.x_data,
          y=Data.bp_mean,
          marker = dict(color = "rgba(0, 0, 200, 0.9)", )
        ) 

      ],
      layout=go.Layout(
        title="Артериално налягане",
        yaxis_title="BP mm/Hg",
        showlegend=False,
        #xaxis_title="Време"    
      )
    )
    self.plot_1.figure = fig3

    #  snipets
    '''    MEAN preassure
        go.Scatter(
          name="BP-M",
          x=Data.x_data,
          y=Data.bp_mean,
          marker = dict(color = "rgba(0, 0, 200, 0.9)", )
        ) 
    '''
    '''
    self.plot_1.data = [
    go.Bar(
    x = Data.bp_dat,
    y = Data.bp_sys,
    name="BP",
    color= 'rgb(16, 32, 77)',
    marker = dict(
      color= 'rgba(200,09, 0, 0.2)',         # color= 'rgb(16, 32, 77)'      
      )
    ), 
    ]
    '''
  