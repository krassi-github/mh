from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import plotly.graph_objects as go
from .. import Data


class Form1(Form1Template):
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    print("Start Init()")
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    #self.column_panel_2.width = "default"
    #self.b_up.width = "80"
    #self.b_up.text = "   "
    #self.b_dn.width = "60"
    self.column_panel_2.row_spacing = 4
    self.label_1.text = self.column_panel_2.width
    self.show_summary()
    Data.set_bp_list()
    self.repeating_panel_1.items = Data.bp_list  # [{}]
    self.color_rows(self.repeating_panel_1)
    self.plot_1_show()

  def color_rows(self, rep):
    for i, r in enumerate(rep.get_components()):
      if not i%2:
        r.background = "rgba(69,183,249,0.1)"  #'theme:Gray 200'     


  def show_summary(self):
    self.lb_22.text = Data.bp_sys[0]
    self.lb_23.text = Data.bp_sys[1]
    self.lb_24.text = Data.bp_sys[2]
    self.lb_25.text = Data.bp_sys[3]
    
    self.lb_32.text = Data.bp_sys[0]
    self.lb_33.text = Data.bp_sys[1]
    self.lb_34.text = Data.bp_sys[2]
    self.lb_35.text = Data.bp_sys[3]

  def b_up_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def b_dn_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  clrs = ['rgb(255,0,0)','rgb(0,255,0)','rgb(0,0,255)']    # ,'rgb(0,100,0)','rgb(0,100,0)','rgb(0,100,0)']
  def plot_1_show(self):     
    self.label_1.text += "  plot_1"
    #bp_color
    fig3 = go.Figure(
      data=[
        go.Bar(
          name="BP-D",
          x=Data.bp_dat,
          y=Data.bp_dia,
          offsetgroup=0,
          marker = dict(color = "rgba(10, 10, 10, 0.1)", )
        ),
        go.Bar(
          name="BP-S",
          x=Data.bp_dat,
          y=Data.bp_sys_add,
          offsetgroup=0,
          base = Data.bp_dia,          
          marker = dict(color = self.clrs, )
        ),
        go.Scatter(
          name="BP-M",
          x=Data.bp_dat,
          y=Data.bp_mea,
          marker = dict(color = "rgba(0, 0, 200, 1.9)", )
        )
      ],
      layout=go.Layout(
        title="Артериално налягане",
        yaxis_title="BP mm/Hg",
        #xaxis_title="Време"    
      )
    )
    self.plot_1.figure = fig3
  
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
  